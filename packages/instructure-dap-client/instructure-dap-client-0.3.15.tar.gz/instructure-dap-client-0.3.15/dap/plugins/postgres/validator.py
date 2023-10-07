from dap.integration.connection import AbstractQueryExecutor
from dap.integration.database_errors import (
    NonExistingTableError,
    TableAlreadyExistsError,
)
from dap.integration.validator import AbstractDatabaseValidator
from dap.plugins.sqlalchemy.queries import SqlAlchemySyncQuery
from sqlalchemy import Connection, Inspector, inspect
from sqlalchemy.ext.asyncio import AsyncConnection


def table_exists(db_conn: Connection, table_name: str, schema: str) -> bool:
    inspector: Inspector = inspect(db_conn)
    return inspector.has_table(table_name, schema)


class DatabaseValidator(AbstractDatabaseValidator):
    _db_connection: AbstractQueryExecutor[AsyncConnection]
    _table_name: str
    _schema: str

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        schema: str,
        table_name: str,
    ) -> None:
        self._db_connection = db_connection
        self._table_name = table_name
        self._schema = schema

    async def validate_init(self) -> None:
        await self._db_connection.execute(
            SqlAlchemySyncQuery[None](
                lambda connection: self._check_table(
                    connection, self._table_name, self._schema, False
                )
            )
        )

    async def validate_sync(self) -> None:
        await self._db_connection.execute(
            SqlAlchemySyncQuery[None](
                lambda connection: self._check_table(
                    connection, self._table_name, self._schema, True
                )
            )
        )

    @staticmethod
    def _check_table(
        connection: Connection, table_name: str, table_schema: str, should_exist: bool
    ) -> None:
        if not should_exist and table_exists(connection, table_name, table_schema):
            raise TableAlreadyExistsError(table_name, table_schema)
        elif should_exist and not table_exists(connection, table_name, table_schema):
            raise NonExistingTableError(table_schema, table_name)
