import logging
from datetime import datetime
from ipaddress import ip_address
from typing import Any, Callable, List, Optional, Type, TypeVar
from uuid import UUID

import orjson
from sqlalchemy import ARRAY, JSON, TIMESTAMP, BigInteger, Boolean, Column, Double
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, SmallInteger, String, Uuid
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql.type_api import TypeEngine

from .integration.base_processor import TsvRecord
from .timestamp import clamp_naive_datetime, valid_naive_datetime

T = TypeVar("T")

logger = logging.getLogger("dap")

TsvColumnCast = Callable[[Optional[bytes]], Any]
TsvRecordExtractor = Callable[[TsvRecord], Any]


def _handle_exceptional_tsv_datetime(
    record_tsv: TsvRecord, key_indices: List[int], value: bytes
) -> datetime:
    # Ignore type check here since we know that the primary key cannot be None.
    keys = tuple(record_tsv[key_index].decode("utf-8") for key_index in key_indices)  # type: ignore
    str_value = value.decode("utf-8")
    clamped_value = clamp_naive_datetime(str_value)
    logger.warning(
        f"Timestamp format error encountered in record {keys}: {str_value} converted to {clamped_value}"
    )
    return clamped_value


def _get_primary_tsv_column_extractor(
    column_index: int, type_cast: Optional[TsvColumnCast]
) -> TsvRecordExtractor:
    """
    Helps extract a value to be inserted into a primary key column.

    :returns: A lambda function that extracts the value from a TSV record.
    """

    if type_cast is None:
        return lambda record_tsv: record_tsv[column_index]
    else:
        cast = type_cast  # hint to type checker
        return lambda record_tsv: cast(record_tsv[column_index])


def _get_required_tsv_column_extractor(
    key_indices: List[int],
    column_index: int,
    column_type: Type[TypeEngine],
    type_cast: Optional[TsvColumnCast],
) -> TsvRecordExtractor:
    """
    Helps extract a required value to be inserted into a non-nullable column.

    :returns: A lambda function that extracts the value from a TSV record.
    """

    if type_cast is None:
        return lambda record_tsv: record_tsv[column_index]
    elif column_type is TIMESTAMP:
        cast = type_cast  # hint to type checker

        def _get_required_tsv_timestamp_value(record_tsv: TsvRecord) -> datetime:
            value = record_tsv[column_index]
            try:
                return cast(value)
            except ValueError:
                # Ignore type check here since we know that the column is required hence it cannot be None.
                return _handle_exceptional_tsv_datetime(record_tsv, key_indices, value)  # type: ignore

        return _get_required_tsv_timestamp_value
    else:
        cast = type_cast  # hint to type checker
        return lambda record_tsv: cast(record_tsv[column_index])


def _get_optional_tsv_column_extractor(
    key_indices: List[int],
    column_index: int,
    column_type: Type[TypeEngine],
    type_cast: Optional[TsvColumnCast],
) -> TsvRecordExtractor:
    """
    Helps extract an optional value to be inserted into a nullable column.

    :returns: A lambda function that extracts the value from a TSV record.
    """

    if type_cast is None:
        return lambda record_tsv: record_tsv[column_index]
    elif column_type is TIMESTAMP:
        cast = type_cast  # hint to type checker

        def _get_optional_tsv_timestamp_value(
            record_tsv: TsvRecord,
        ) -> Optional[datetime]:
            value = record_tsv[column_index]
            if value is None:
                return None

            try:
                return cast(value)
            except ValueError:
                return _handle_exceptional_tsv_datetime(record_tsv, key_indices, value)

        return _get_optional_tsv_timestamp_value
    else:
        cast = type_cast  # hint to type checker

        def _get_optional_tsv_value(record_tsv: TsvRecord) -> Optional[Any]:
            value = record_tsv[column_index]
            if value is None:
                return None
            return cast(value)

        return _get_optional_tsv_value


def get_tsv_column_extractor(
    key_indices: List[int], column_index: int, column_def: Column
) -> TsvRecordExtractor:
    """
    Returns a lambda function that extracts a column value from a TSV record.

    The input to the returned lambda function is a TSV record, which can be `bytes` or `None`. The output shall be one of
    the following types: `list`, `int`, `float`, `str`, `bool` or `None`. For example,

    ```tsv
    23 Budapest 1112
    ```

    The objective of the lambda is to extract primary key column values from `key` and other column values from
    `value`, and perform any further transformations before the value can be forwarded to `asyncpg`. Most types
    such as `int` or `str` don't require any mutation. However, `datetime` needs to be converted into a naive
    (timezone-unaware) representation for `asyncpg` to pass it on as a database `timestamp without time zone`.

    :returns: A lambda function that extracts the value from a JSON record in the right format and as the right type.
    """

    column_type = type(column_def.type)
    type_cast: Optional[TsvColumnCast] = get_tsv_type_cast(column_type)

    # make sure to return a single lambda that takes a record and returns the value directly
    # perform as much pre-processing outside the lambda as possible, avoid expensive computations within the lambda
    if column_def.primary_key:
        return _get_primary_tsv_column_extractor(column_index, type_cast)
    elif column_def.nullable:
        return _get_optional_tsv_column_extractor(
            key_indices, column_index, column_type, type_cast
        )
    else:
        return _get_required_tsv_column_extractor(
            key_indices, column_index, column_type, type_cast
        )


def get_tsv_type_cast(column_type: Type[TypeEngine]) -> Optional[TsvColumnCast]:
    type_cast: Optional[TsvColumnCast]
    if (
        column_type is Integer
        or column_type is SmallInteger
        or column_type is BigInteger
    ):
        # original TSV type: `bytes` (containing the string representation of an integer)
        # deserialized Python type: `int`
        # database type: an integer type (storage size set based on schema)
        type_cast = int  # type: ignore
    elif column_type is Float or column_type is Double:
        # original TSV type: `bytes` (containing the string representation of a floating-point number)
        # deserialized Python type: `int` or `float` (depending on presence of fractional digits)
        # database type: a floating-point type (storage size set based on schema)
        # use conversion to ensure the proper type when passing to database
        type_cast = float  # type: ignore
    elif column_type is String:
        # original TSV type: `bytes` (containing the string encoded in UTF-8)
        # deserialized Python type: `bytes`
        # database type: `varchar` or `text`
        type_cast = None
    elif column_type is SqlEnum:
        # original TSV type: `bytes` (containing the string encoded in UTF-8)
        # deserialized Python type: `bytes`
        # database type: `anyenum`
        # passed to database driver as `bytes`, to be converted to enumeration type by database
        type_cast = None
    elif column_type is JSON:
        # original TSV type: `bytes` (containing the JSON content as string encoded in UTF-8)
        # deserialized Python type: `bytes` (containing the JSON content as string encoded in UTF-8)
        # database type: `jsonb`
        # converted back to `str` to pass to database as `jsonb`
        type_cast = None
    elif column_type is TIMESTAMP:
        # original TSV type: `bytes` (format: ISO-8601 and RFC 3339 compliant string encoded in UTF-8)
        # deserialized Python type: `datetime`
        # database type: `timestamp without time zone`
        # converted to naive `datetime` to pass to database
        # Ignoring type because we know that `type_cast` will be used only if `value` is not `None`
        type_cast = lambda value: valid_naive_datetime(value.decode("utf-8"))  # type: ignore
    elif column_type is Boolean:
        # original TSV type: `bytes` (containing the string representation of a boolean encoded in UTF-8)
        # deserialized Python type: `bool`
        type_cast = lambda value: value == b"true"
    elif column_type is INET:
        # original TSV type: `bytes` (containing the string representation of an IP address encoded in UTF-8)
        # deserialized Python type: `IPV4Address` or `IPV6Address`
        # database type: inet
        # Ignoring type because we know that `type_cast` will be used only if `value` is not `None`
        type_cast = lambda value: ip_address(value.decode("utf-8"))  # type: ignore
    elif column_type is Uuid:
        # original TSV type: `bytes` (containing the string representation of a UUID encoded in UTF-8)
        # deserialized Python type: `uuid`
        # database type: uuid
        # Ignoring type because we know that `type_cast` will be used only if `value` is not `None`
        type_cast = lambda value: UUID(value.decode("ascii"))  # type: ignore
    elif column_type is ARRAY:
        # original TSV type: `bytes` (containing the string representation of a JSON array encoded in UTF-8)
        # deserialized Python type: `list` (nested)
        # convert elements recursively
        type_cast = lambda value: orjson.loads(value)  # type: ignore
    else:
        raise TypeError(f"cannot convert to {column_type}")

    return type_cast
