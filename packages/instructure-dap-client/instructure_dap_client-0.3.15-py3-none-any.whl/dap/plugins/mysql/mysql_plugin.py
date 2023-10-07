import logging
from typing import Optional

from dap.dap_types import Format, TableQuery, VersionedSchema
from dap.integration.connection import AbstractDatabaseConnection
from dap.integration.database_errors import DatabaseConnectionError
from dap.integration.meta_table import AbstractMetaTableManager
from dap.integration.plugin import DatabasePlugin
from dap.integration.processor import AbstractProcessor
from dap.integration.validator import AbstractDatabaseValidator
from dap.plugins.sqlalchemy.connection import SqlAlchemyConnection

from .init_processor import MysqlInitProcessor
from .meta_table import MysqlMetaTableManager
from .sync_processor import MysqlSyncProcessor
from .validator import MysqlDatabaseValidator

logger = logging.getLogger("dap")


class MysqlPlugin(DatabasePlugin):
    _connection: Optional[SqlAlchemyConnection]
    __warning_displayed: bool = False
    __tables_without_namespace_prefix = ["canvas", "canvas_logs"]

    def __init__(self) -> None:
        if not MysqlPlugin.__warning_displayed:
            logger.warning(
                "⚠️Warning: aiomysql is classified as being in alpha development status. Instructure cannot "
                "assume responsibility for any potential changes or consequences resulting from its usage."
            )
            MysqlPlugin.__warning_displayed = True
        self._connection = None
        self._database_name = ""

    def connect(self, connection_string: str) -> None:
        if self._connection is not None:
            raise DatabaseConnectionError("already connected to the database")

        self._connection = SqlAlchemyConnection(
            connection_string, {"mysql": "aiomysql"}
        )
        # in mysql there is no concept of schema, so the database name is used as schema
        database_name = self._connection.get_database_name()
        if database_name is None:
            raise DatabaseConnectionError(
                "database name not found in connection string"
            )
        self._database_name = database_name

    def get_connection(self) -> AbstractDatabaseConnection:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return self._connection

    def create_metatable_manager(
        self, namespace: str, table: str
    ) -> AbstractMetaTableManager:
        table = self.get_table_name(namespace, table)
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return MysqlMetaTableManager(self._connection, self._database_name, table)

    def create_init_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractProcessor:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        table = self.get_table_name(namespace, table)
        return MysqlInitProcessor(self._connection, self._database_name, table, schema)

    def create_sync_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractProcessor:
        table = self.get_table_name(namespace, table)
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return MysqlSyncProcessor(self._connection, self._database_name, table, schema)

    def create_database_validator(
        self, namespace: str, table: str
    ) -> AbstractDatabaseValidator:
        table = self.get_table_name(namespace, table)
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return MysqlDatabaseValidator(self._connection, self._database_name, table)

    def get_snapshot_query(self) -> TableQuery:
        return TableQuery(format=Format.JSONL, filter=None)

    def get_incremental_query(self) -> TableQuery:
        return TableQuery(format=Format.JSONL, filter=None)

    async def disconnect(self) -> None:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        await self._connection.close()
        self._connection = None

    def get_table_name(self, namespace: str, table: str) -> str:
        if namespace in MysqlPlugin.__tables_without_namespace_prefix:
            return table
        return f"{namespace}__{table}"
