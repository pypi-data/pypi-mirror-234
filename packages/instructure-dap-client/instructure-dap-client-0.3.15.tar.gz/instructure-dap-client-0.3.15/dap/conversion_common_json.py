import logging
import typing
from datetime import datetime
from ipaddress import ip_address
from typing import Any, Callable, Dict, Optional, Type, TypeVar
from uuid import UUID

import orjson
from sqlalchemy import (
    ARRAY,
    BINARY,
    DATETIME,
    JSON,
    TEXT,
    TIMESTAMP,
    VARCHAR,
    BigInteger,
    Boolean,
    Column,
    Double,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, SmallInteger, String, Uuid
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql.type_api import TypeEngine
from strong_typing.core import JsonType

from .integration.base_processor import JsonRecord
from .timestamp import clamp_naive_datetime, valid_naive_datetime

T = TypeVar("T")

logger = logging.getLogger("dap")

JsonTypeCast = Callable[[JsonType], Any]
JsonRecordExtractor = Callable[[JsonRecord], Any]
JsonRecordExtractorDict = Dict[str, JsonRecordExtractor]
JsonValueConverter = Callable[[JsonType], Any]


def _handle_exceptional_json_datetime(
    record_json: JsonRecord, column_name: str
) -> datetime:
    key = record_json["key"]
    value = typing.cast(str, record_json["value"][column_name])
    clamped_value = clamp_naive_datetime(value)
    logger.warning(
        f"Timestamp format error encountered in record {key}: {value} converted to {clamped_value}"
    )
    return clamped_value


def _get_primary_json_column_extractor(
    column_name: str, type_cast: Optional[JsonTypeCast]
) -> JsonRecordExtractor:
    """
    Helps extract a value to be inserted into a primary key column.

    :returns: A lambda function that extracts the value from a JSON record.
    """

    if type_cast is None:
        return lambda record_json: record_json["key"][column_name]
    else:
        cast = type_cast  # hint to type checker
        return lambda record_json: cast(record_json["key"][column_name])


def _get_required_json_column_extractor(
    column_name: str,
    column_type: Type[TypeEngine],
    type_cast: Optional[JsonTypeCast],
) -> JsonRecordExtractor:
    """
    Helps extract a required value to be inserted into a non-nullable column.

    :returns: A lambda function that extracts the value from a JSON record.
    """

    if type_cast is None:
        return lambda record_json: record_json["value"][column_name]
    elif column_type is TIMESTAMP or column_type is DATETIME:
        cast = type_cast  # hint to type checker

        def _get_required_json_timestamp_value(record_json: JsonRecord) -> datetime:
            value = record_json["value"][column_name]
            try:
                return cast(value)
            except ValueError:
                return _handle_exceptional_json_datetime(record_json, column_name)

        return _get_required_json_timestamp_value
    else:
        cast = type_cast  # hint to type checker
        return lambda record_json: cast(record_json["value"][column_name])


def _get_optional_json_column_extractor(
    column_name: str, column_type: Type[TypeEngine], type_cast: Optional[JsonTypeCast]
) -> JsonRecordExtractor:
    """
    Helps extract an optional value to be inserted into a nullable column.

    :returns: A lambda function that extracts the value from a JSON record.
    """

    if type_cast is None:
        return lambda record_json: record_json["value"].get(column_name)
    elif column_type is TIMESTAMP or column_type is DATETIME:
        cast = type_cast  # hint to type checker

        def _get_optional_timestamp_json_value(
            record_json: JsonRecord,
        ) -> Optional[datetime]:
            value = record_json["value"].get(column_name)
            if value is None:
                return None

            try:
                return cast(value)
            except ValueError:
                return _handle_exceptional_json_datetime(record_json, column_name)

        return _get_optional_timestamp_json_value
    else:
        cast = type_cast  # hint to type checker

        def _get_optional_value(record_json: JsonRecord) -> Optional[Any]:
            value = record_json["value"].get(column_name)
            if value is None:
                return None
            return cast(value)

        return _get_optional_value


def _json_dump(value: Any) -> str:
    return orjson.dumps(value, option=orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z).decode(
        "utf-8"
    )


def _uuid_to_binary(value: str) -> bytes:
    """
    Converts a UUID string to a binary representation.
    Used to store UUIDs in a binary column if a database engine does not support UUIDs natively (e.g. MySQL).
    :param value: UUID string
    :return: Binary representation of the UUID
    """
    return UUID(value).bytes


def get_json_column_extractor(col: Column) -> JsonRecordExtractor:
    """
    Returns a lambda function that extracts a column value from the deserialized JSON representation of a record.

    The input to the returned lambda function is a deserialized JSON representation obtained by `orjson.loads`, which
    deserializes (recursively) to `dict`, `list`, `int`, `float`, `str`, `bool`, and `None` objects. For example,

    ```json
    { "key": { "id": 23 }, "value": { "city": "Budapest", "zip": 1112 } }
    ```

    The objective of the lambda is to extract primary key column values from `key` and other column values from
    `value`, and perform any further transformations before the value can be forwarded to `asyncpg`. Most types
    such as `int` or `str` don't require any mutation. However, `datetime` needs to be converted into a naive
    (timezone-unaware) representation for `asyncpg` to pass it on as a database `timestamp without time zone`.

    :returns: A lambda function that extracts the value from a JSON record in the right format and as the right type.
    """

    column_type = type(col.type)
    type_cast: Optional[JsonTypeCast] = get_json_type_cast(column_type)

    # make sure to return a single lambda that takes a record and returns the value directly
    # perform as much pre-processing outside the lambda as possible, avoid expensive computations within the lambda
    column_name = col.name
    if col.primary_key:
        return _get_primary_json_column_extractor(column_name, type_cast)
    elif col.nullable:
        return _get_optional_json_column_extractor(column_name, column_type, type_cast)
    else:
        return _get_required_json_column_extractor(column_name, column_type, type_cast)


def get_json_type_cast(column_type: Type[TypeEngine]) -> Optional[JsonTypeCast]:
    type_cast: Optional[JsonTypeCast]
    if (
        column_type is Integer
        or column_type is SmallInteger
        or column_type is BigInteger
    ):
        # original JSON type: `integer` (a specialization of `number`)
        # deserialized Python type: `int`
        # database type: an integer type (storage size set based on schema)
        type_cast = None
    elif column_type is Float or column_type is Double:
        # original JSON type: `number`
        # deserialized Python type: `int` or `float` (depending on presence of fractional digits)
        # database type: a floating-point type (storage size set based on schema)
        # use conversion to ensure the proper type when passing to database
        type_cast = float  # type: ignore
    elif column_type is String:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: `varchar` or `text`
        type_cast = None
    elif column_type is SqlEnum:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: `anyenum`
        # passed to database driver as `str`, to be converted to enumeration type by database
        type_cast = None
    elif column_type is JSON:
        # original JSON type: `object` (nested)
        # deserialized Python type: `dict` (nested)
        # database type: `jsonb`
        # converted back to `str` to pass to database as `jsonb`
        type_cast = _json_dump
    elif column_type is TIMESTAMP or column_type is DATETIME:
        # original JSON type: `str` (format: ISO-8601 and RFC 3339 compliant string)
        # deserialized Python type: `str`
        # database type: `timestamp without time zone`
        # converted to naive `datetime` to pass to database
        type_cast = valid_naive_datetime  # type: ignore
    elif column_type is Boolean:
        # original JSON type: `boolean`
        # deserialized Python type: `bool`
        type_cast = None
    elif column_type is INET:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: inet
        type_cast = ip_address  # type: ignore[assignment]
    elif column_type is Uuid:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: uuid
        type_cast = UUID  # type: ignore[assignment]
    elif column_type is ARRAY:
        # original JSON type: `array` (nested)
        # deserialized Python type: `list` (nested)
        # convert elements recursively
        type_cast = None
    elif column_type is TEXT:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: TEXT
        type_cast = None
    elif column_type is MEDIUMTEXT:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: MEDIUMTEXT
        type_cast = None
    elif column_type is VARCHAR:
        # original JSON type: `string`
        # deserialized Python type: `str`
        # database type: VARCHAR
        type_cast = None
    elif column_type is BINARY:
        # original JSON type: `string
        # deserialized Python type: `str`
        # database type: BINARY
        # NOTE: BINARY is only used for a special case here: to store binary UUIDs in databases which don't support
        #       storing out UUIDs in the native UUID type. In this case, the UUID is converted from a string to bytes
        type_cast = _uuid_to_binary  # type: ignore[assignment]
    else:
        raise TypeError(f"cannot convert to {column_type}")

    return type_cast
