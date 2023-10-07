import datetime
from typing import AsyncIterator, List, Tuple

import aiomysql
from dap import timestamp
from dap.conversion_perf import create_copy_converters
from dap.dap_types import VersionedSchema
from dap.integration.base_processor import JSONLRecordProcessor, JsonRecord
from dap.integration.connection import AbstractQueryExecutor
from dap.integration.processor import ContextAwareObject
from dap.plugins.sqlalchemy.queries import SqlAlchemySyncQuery
from dap.timer import Timer
from sqlalchemy import Connection, Inspector, Table, inspect
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.ddl import CreateSchema

from .metadata import create_table_definition
from .queries import AioMysqlQuery


def _create_tables(conn: Connection, table_def: Table) -> None:
    inspector: Inspector = inspect(conn)

    # In MySQL the maximum length of a column comment is 1024 characters
    # Truncate the column comment to 1024 characters if it is longer
    for col in table_def.columns._all_columns:
        if col.comment is not None and len(col.comment) > 1024:
            col.comment = col.comment[:1024]

    if table_def.schema is not None and not inspector.has_schema(table_def.schema):
        conn.execute(CreateSchema(table_def.schema))  # type: ignore

    table_def.metadata.create_all(conn)


class MysqlInitProcessor(JSONLRecordProcessor):
    """
    Creates and populates an empty database table with records acquired from the DAP service.
    """

    _db_connection: AbstractQueryExecutor[AsyncConnection]
    _table_def: Table
    _converters: Tuple

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, table_schema)
        self._converters = create_copy_converters(self._table_def)
        # In mysql the range for DATETIME values is '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.499999',
        # https://dev.mysql.com/doc/refman/8.0/en/datetime.html#:~:text=MySQL%20retrieves%20and%20displays%20DATETIME,23%3A59%3A59'%20.
        timestamp.DATETIME_MIN = datetime.datetime.min.replace(year=1000)
        timestamp.DATETIME_MAX = datetime.datetime.max.replace(microsecond=499999)

    async def prepare(self) -> None:
        await self._db_connection.execute(
            SqlAlchemySyncQuery[None](
                lambda connection: _create_tables(connection, self._table_def)
            )
        )

    async def process_impl(
        self, obj: ContextAwareObject, records: AsyncIterator[JsonRecord]
    ) -> None:
        async with Timer(f"inserting records from {obj}"):
            await self._db_connection.execute(
                AioMysqlQuery[None](
                    lambda connection: self._execute_with_connection(
                        records, connection
                    )
                )
            )

    async def _execute_with_connection(
        self, records: AsyncIterator[JsonRecord], connection: aiomysql.Connection
    ) -> None:
        insert_query = f"INSERT INTO `{self._table_def.name}` ({', '.join(col.name for col in self._table_def.columns)}) VALUES ({', '.join(['%s' for _ in self._table_def.columns])})"
        records_to_insert = await self._convert_records(records)

        async with connection.cursor() as cursor:
            await cursor.executemany(insert_query, records_to_insert)

    async def _convert_records(self, records: AsyncIterator[JsonRecord]) -> List[Tuple]:
        records_list = []
        async for record in records:
            records_list.append(
                tuple(converter(record) for converter in self._converters)
            )
        return records_list

    async def close(self) -> None:
        pass
