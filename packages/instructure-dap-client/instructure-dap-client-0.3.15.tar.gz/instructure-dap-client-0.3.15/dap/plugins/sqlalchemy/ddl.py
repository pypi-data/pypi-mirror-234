import logging
from typing import Any, Optional

from sqlalchemy import bindparam, column, table

logger = logging.getLogger("dap")


def table_name(name: str, schema: Optional[str] = None) -> str:
    table_name_str = str(table(name=name, schema=schema))
    return table_name_str


def column_name(name: str) -> str:
    column_name_str = str(column(name))
    return column_name_str


def type_name(name: str, schema: Optional[str] = None) -> str:
    # Fully qualified type names has the same format (schema.name) so we can reuse the table_name function here.
    return table_name(name, schema)


def value_literal(value: Any) -> str:
    value_str = (
        bindparam("value", value).compile(compile_kwargs={"literal_binds": True}).string
    )
    return value_str
