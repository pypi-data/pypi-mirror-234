from fastapi import FastAPI, Request, status
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from urllib.parse import urlsplit


class SetRootPathMiddleware(BaseHTTPMiddleware):
    """
    Set `root_path` to make proper URLs behind a proxy
    https://fastapi.tiangolo.com/advanced/behind-a-proxy/
    """

    async def dispatch(self, request: Request, call_next):
        original_url = request.headers.get("x-envoy-original-path")
        path = request.url.path

        if original_url:
            original_path = urlsplit(original_url).path

            if original_path.endswith(path):
                request.scope["root_path"] = original_path.removesuffix(path)

        return await call_next(request)


class App(FastAPI):
    def setup(self) -> None:
        if not self.swagger_ui_init_oauth:
            self.swagger_ui_init_oauth = {"clientId": "delphai-api"}

        super().setup()

        self.add_middleware(SetRootPathMiddleware)
        self.add_event_handler("startup", self._include_dependency_responses)

        try:
            import httpx
        except ImportError:
            pass
        else:
            self.add_exception_handler(httpx.TimeoutException, self._timeout_error)

    def _include_dependency_responses(self):
        for route in self.routes:
            if isinstance(route, APIRoute):
                for dependency in self._walk_dependency_tree(route.dependant):
                    dependency_responses = getattr(dependency.call, "responses", None)
                    if dependency_responses:
                        route.responses = dict(dependency_responses, **route.responses)

                endpoint_responses = getattr(route.endpoint, "responses", None)
                if endpoint_responses:
                    route.responses = dict(endpoint_responses, **route.responses)

    def _walk_dependency_tree(self, dependant, visited=None):
        if visited is None:
            visited = set()
        visited.add(dependant.cache_key)

        for sub_dependant in dependant.dependencies:
            if sub_dependant.cache_key in visited:
                continue

            yield sub_dependant
            yield from self._walk_dependency_tree(sub_dependant, visited)

    def _timeout_error(self, request, error):
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "Gateway Timeout"},
        )
