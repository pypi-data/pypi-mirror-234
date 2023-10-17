from bson.objectid import ObjectId as BsonObjectId
import uuid
from fastapi import Query, Depends
from typing import Tuple


class ObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return str(BsonObjectId(v))

    @classmethod
    def __modify_schema__(cls, field_schema, field):
        field_schema.update(
            type="string",
            minLength=24,
            maxLength=24,
            pattern="^[0-9a-fA-F]{24}$",
        )

        if "example" not in field.field_info.extra:
            field_schema["example"] = field.field_info.extra[
                "example"
            ] = "5ecd2d2d0faf391eadb211a7"


class UUID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return str(uuid.UUID(v))

    @classmethod
    def __modify_schema__(cls, field_schema, field):
        field_schema.update(
            type="string",
            minLength=37,
            maxLength=37,
            pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        )

        if "example" not in field.field_info.extra:
            field_schema["example"] = field.field_info.extra[
                "example"
            ] = "ec8ccc64-81dc-4b7b-a72e-daa7172bfae6"


def LimitOffset(limit_default=20, limit_max=300):  # noqa: N802
    @Depends
    def get_limit_offset(
        limit: int = Query(
            default=limit_default,
            ge=0,
            le=limit_max,
            description="The maximum number of entries to be returned per call",
            example=limit_default,
        ),
        offset: int = Query(
            default=0,
            ge=0,
            description="The (zero-based) offset of the first item returned in the collection",  # noqa: E501
            example=0,
        ),
    ) -> Tuple[int, int]:
        return limit, offset

    return get_limit_offset
