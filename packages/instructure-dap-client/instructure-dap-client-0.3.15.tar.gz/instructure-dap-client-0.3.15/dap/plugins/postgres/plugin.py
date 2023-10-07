from typing import Optional

from dap.dap_types import Format, TableQuery, VersionedSchema
from dap.integration.connection import AbstractDatabaseConnection
from dap.integration.database_errors import DatabaseConnectionError
from dap.integration.meta_table import AbstractMetaTableManager
from dap.integration.plugin import DatabasePlugin
from dap.integration.processor import AbstractProcessor
from dap.integration.validator import AbstractDatabaseValidator
from dap.plugins.sqlalchemy.connection import SqlAlchemyConnection

from .init_processor import InitProcessor
from .meta_table import MetaTableManager
from .sync_processor import SyncProcessor
from .validator import DatabaseValidator


class PostgresPlugin(DatabasePlugin):
    _connection: Optional[SqlAlchemyConnection]

    def __init__(self) -> None:
        self._connection = None

    def connect(self, connection_string: str) -> None:
        if self._connection is not None:
            raise DatabaseConnectionError("already connected to the database")

        self._connection = SqlAlchemyConnection(
            connection_string, {"postgresql": "asyncpg"}
        )

    def get_connection(self) -> AbstractDatabaseConnection:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return self._connection

    def create_metatable_manager(
        self, namespace: str, table: str
    ) -> AbstractMetaTableManager:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return MetaTableManager(self._connection, namespace, table)

    def create_init_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractProcessor:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return InitProcessor(self._connection, namespace, table, schema)

    def create_sync_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractProcessor:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return SyncProcessor(self._connection, namespace, table, schema)

    def create_database_validator(
        self, namespace: str, table: str
    ) -> AbstractDatabaseValidator:
        if self._connection is None:
            raise DatabaseConnectionError("not connected to the database")
        return DatabaseValidator(self._connection, namespace, table)

    def get_snapshot_query(self) -> TableQuery:
        return TableQuery(format=Format.JSONL, filter=None)

        # TODO: to be used when full TSV support is enabled on the backend.
        # return TableQuery(format=Format.TSV, filter=None)

    def get_incremental_query(self) -> TableQuery:
        return TableQuery(format=Format.JSONL, filter=None)
