import abc
from datetime import datetime

from ..dap_types import GetTableDataResult, VersionedSchema


class AbstractMetaTableManager(abc.ABC):
    """
    Interface for meta-table management.

    The meta-table is a table in the local database that shall register the following information about the replicated
    DAP tables:

        - namespace: The namespace of the source table exposed by DAP API (e.g. `canvas`).
        - source_table: The name of the source table exposed by DAP API (e.g. `accounts`).
        - timestamp: The timestamp of the source table that can be used by the client library in incremental queries
          during subsequent `syncdb` command executions.
        - schema_version: The latest schema version of the source table at the time point when it was last initialized
          or synchronized with the DAP API.
        - target_schema: The name of the target schema in the local database if applicable (e.g. in case of
          a PostgreSQL database the tables can be grouped into schemas).
        - target_table: The name of the target table in the local database. In might differ from the name of the source
          table. For example in case of a MySQL database, the tables cannot be grouped in schemas. In this case,
          the implementor can use a prefix that reflects the namespace of the source table. For example, the qualified
          name `canvas.accounts` would become `canvas__accounts`.
        - schema_description: The latest schema descriptor of the source table at the time point when it was
          initialized or last synchronized.
        - schema_description_format: The format of the schema descriptor (e.g. `json`).
    """

    @abc.abstractmethod
    async def get_timestamp(self) -> datetime:
        """
        Gets the timestamp (in UTC format) of the source table that can be used by the client library in incremental
        queries in subsequent `syncdb` command executions.

        :returns: The timestamp in UTC format.
        """
        ...

    @abc.abstractmethod
    async def initialize(
        self,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        """
        Creates the meta-table in the local database (unless already created) and adds an entry about the source table.

        :param table_schema: The current schema of the source table returned by the DAP API.
        :param table_data: The result of the DAP API snapshot query of the source table containing the current
          schema version and timestamp.
        """
        ...

    @abc.abstractmethod
    async def synchronize(
        self,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        """
        Updates the timestamp, schema version and schema descriptor of the source table entry in the meta-table.

        :param table_schema: The current schema of the source table returned by the DAP API.
        :param table_data: The result of the DAP API incremental query of the source table containing the current
          schema version and timestamp.
        """
        ...

    @abc.abstractmethod
    async def drop(self) -> None:
        """
        Drops the entry about the source table from the meta-table and drops the corresponding target table as well.
        """
        ...
