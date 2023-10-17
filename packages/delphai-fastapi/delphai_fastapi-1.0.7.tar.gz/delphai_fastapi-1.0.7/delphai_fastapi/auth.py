import httpx
import logging

from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JOSEError, jwt

from .decorators import returns_errors


TokenPayload = Optional[dict[str, Any]]

logger = logging.getLogger(__file__)

AUTH_BASE_URL = "https://auth.delphai.com/auth/realms/delphai/protocol/openid-connect"

OAuth2Token = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{AUTH_BASE_URL}/auth",
    tokenUrl=f"{AUTH_BASE_URL}/token",
    auto_error=False,
)


@Depends
@returns_errors(
    status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN
)
async def validated_token(
    token: Annotated[str, Depends(OAuth2Token)],
) -> TokenPayload:
    if not token:
        return {}

    try:
        payload = await decode_token(token)
        payload["_token"] = token
        return payload

    except JOSEError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    except (TypeError, KeyError):
        logger.warning("Wrong token format")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@Depends
class Authorization:
    def __init__(
        self, request: Request, token_payload: Annotated[TokenPayload, validated_token]
    ):
        self._request = request

        self._token_payload = token_payload

        self._client_id = self._scopes = None
        self._user_id = self._user_email = self._user_name = None
        self._groups = self._roles = None

        if self.is_authenticated:
            self._client_id = token_payload["azp"]
            self._scopes = frozenset(token_payload.get("scope").split())

            self._user_id = token_payload["sub"]
            self._user_email = token_payload.get("email")
            self._user_name = token_payload.get("name")
            self._mongo_user_id = token_payload["mongo_user_id"]
            self._mongo_client_id = token_payload["mongo_client_id"]

            self._groups = frozenset(token_payload.get("group_membership", []))
            self._roles = frozenset(
                token_payload.get("realm_access", {}).get("roles", [])
            )

    def require(self, value):
        if not value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    @property
    def is_direct_request(self):
        return not bool(self._request.headers.get("x-forwarded-for"))

    @property
    def is_authenticated(self):
        return bool(self._token_payload)

    @property
    def token_payload(self):
        return self._token_payload

    @property
    def client_id(self):
        return self._client_id

    @property
    def mongo_client_id(self):
        return self._mongo_client_id

    @property
    def scopes(self):
        return self._scopes

    @property
    def user_id(self):
        return self._user_id

    @property
    def mongo_user_id(self):
        return self._mongo_user_id

    @property
    def user_email(self):
        return self._user_email

    @property
    def user_name(self):
        return self._user_name

    @property
    def groups(self):
        return self._groups

    @property
    def roles(self):
        return self._roles

    @property
    def is_api_client(self):
        return self._request.url.hostname.lower().startswith("api.delphai") and (
            "api" in self.roles
        )


trusted_public_keys = {}


async def decode_token(access_token: str) -> str:
    if not trusted_public_keys:
        await _async_fetch_keys()

    decode_args = {"audience": "delphai-gateway", "options": {"leeway": 10}}

    try:
        return jwt.decode(access_token, trusted_public_keys, **decode_args)
    except JOSEError:
        await _async_fetch_keys()
        return jwt.decode(access_token, trusted_public_keys, **decode_args)


http_client = httpx.AsyncClient()


async def _async_fetch_keys():
    global trusted_public_keys

    response = await http_client.get(f"{AUTH_BASE_URL}/certs")
    response.raise_for_status()
    trusted_public_keys = response.json()
