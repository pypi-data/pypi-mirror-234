from typing import Any, AsyncIterator, Dict, List, TypeVar

from dap.conversion_common_json import JsonRecord, JsonRecordExtractorDict
from dap.conversion_perf import create_delete_converters, create_upsert_converters
from dap.dap_types import VersionedSchema
from dap.integration.base_processor import JSONLRecordProcessor
from dap.integration.connection import AbstractQueryExecutor
from dap.integration.processor import ContextAwareObject
from dap.plugins.sqlalchemy.queries import SqlAlchemyExecutableQuery
from dap.timer import Timer
from sqlalchemy import BindParameter, Delete, Table, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.dml import Insert

from .metadata import create_table_definition

TReturn = TypeVar("TReturn")


class _Parameters:
    upsert_parameters: List[Dict[str, Any]]
    delete_parameters: List[Dict[str, Any]]

    def __init__(self) -> None:
        self.upsert_parameters = []
        self.delete_parameters = []


class SyncProcessor(JSONLRecordProcessor):
    """
    Inserts/updates/deletes records acquired from the DAP service into/in/from a database table.

    Processes synchronization records that can be either UPSERT or DELETE.
    """

    _db_connection: AbstractQueryExecutor[AsyncConnection]
    _table_def: Table
    _upsert_converters: JsonRecordExtractorDict
    _delete_converters: JsonRecordExtractorDict

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, schema)

        self._upsert_converters = create_upsert_converters(self._table_def)
        self._delete_converters = create_delete_converters(self._table_def)

    async def prepare(self) -> None:
        pass

    async def process_impl(
        self, obj: ContextAwareObject, records: AsyncIterator[JsonRecord]
    ) -> None:
        values_clause: Dict[str, BindParameter] = {}
        for col in self._table_def.columns:
            values_clause[col.name] = bindparam(col.name)

        set_clause: Dict[str, BindParameter] = {}
        for col in self._table_def.columns:
            if not col.primary_key:
                set_clause[col.name] = bindparam(col.name)

        upsert_statement: Insert = (
            insert(self._table_def)  # type: ignore
            .values(values_clause)
            .on_conflict_do_update(
                constraint=self._table_def.primary_key, set_=set_clause
            )
        )

        parameters: _Parameters = await self._convert_records(records)
        if parameters.upsert_parameters:
            async with Timer(f"upserting records from {obj}"):
                await self._db_connection.execute(
                    SqlAlchemyExecutableQuery[None](
                        upsert_statement, parameters.upsert_parameters
                    )
                )

        delete_statement: Delete = self._table_def.delete()
        for col in self._table_def.primary_key:
            delete_statement = delete_statement.where(
                self._table_def.c[col.name] == bindparam(col.name)
            )

        if parameters.delete_parameters:
            async with Timer(f"deleting records from {obj}"):
                await self._db_connection.execute(
                    SqlAlchemyExecutableQuery[None](
                        delete_statement, parameters.delete_parameters
                    )
                )

    async def close(self) -> None:
        pass

    async def _convert_records(self, records: AsyncIterator[JsonRecord]) -> _Parameters:
        parameters = _Parameters()
        async for record in records:
            if "value" in record:
                sql_item = {
                    col_name: converter(record)
                    for col_name, converter in self._upsert_converters.items()
                }
                parameters.upsert_parameters.append(sql_item)

            else:
                sql_item = {
                    col_name: converter(record)
                    for col_name, converter in self._delete_converters.items()
                }
                parameters.delete_parameters.append(sql_item)
        return parameters
