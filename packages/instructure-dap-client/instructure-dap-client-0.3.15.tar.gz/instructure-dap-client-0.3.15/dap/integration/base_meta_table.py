import abc
from datetime import datetime
from typing import Generic, TypeVar

from ..dap_types import GetTableDataResult, VersionedSchema
from .connection import AbstractQueryExecutor
from .meta_table import AbstractMetaTableManager

TRawConnection = TypeVar("TRawConnection")


class BaseMetaTableManager(AbstractMetaTableManager, Generic[TRawConnection]):
    """
    The abstract base class that implements the AbstractMetaTableManager interface.

    Plugin developers should typically derive from this class.
    """

    _db_connection: AbstractQueryExecutor[TRawConnection]
    _namespace: str
    _table_name: str

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
    ) -> None:
        self._db_connection = db_connection
        self._namespace = namespace
        self._table_name = table_name

    async def get_timestamp(self) -> datetime:
        return await self.get_timestamp_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
        )

    async def initialize(
        self,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        await self.initialize_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
            table_data,
        )

    async def synchronize(
        self,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        await self.update_table_schema_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
        )
        await self.synchronize_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
            table_data,
        )

    async def drop(self) -> None:
        await self.drop_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
        )

    @abc.abstractmethod
    async def get_timestamp_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
    ) -> datetime:
        """
        Gets the timestamp (in UTC) of the given source table using the given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :returns: The timestamp in UTC format.
        """
        ...

    @abc.abstractmethod
    async def initialize_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        """
        Creates the metatable in the local database (if not yet created) and registers an entry about the given source table using the
        given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The current schema of the source table at the DAP API.
        :param table_data: The result of the DAP API snapshot query of the source table containing the current schema version and timestamp.
        """
        ...

    @abc.abstractmethod
    async def synchronize_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        """
        Updates the timestamp, schema version and schema description of the given source table entry in the metatable using the
        given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The current schema of the source table at the DAP API.
        :param table_data: The result of the DAP API snapshot query of the source table containing the current schema version and timestamp.
        """
        ...

    @abc.abstractmethod
    async def drop_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
    ) -> None:
        """
        Drops the entry about the given source table from the metatable and drops the corresponding target table as well using the given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        """
        ...

    @abc.abstractmethod
    async def update_table_schema_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        """
        Updates the schema of the given source table in the local database using the given database connection if the currently
        registered schema version is lower than the given schema version downloaded from the DAP API.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The new schema description downloaded from the DAP API.
        """
        ...
