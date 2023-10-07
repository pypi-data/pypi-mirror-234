from ..api import DAPSession
from ..downloader import IncrementalClientFactory, SnapshotClientFactory
from ..integration.database import DatabaseConnection
from ..integration.meta_table import AbstractMetaTableManager
from ..integration.processor import AbstractProcessor
from ..integration.validator import AbstractDatabaseValidator


class SQLReplicator:
    """
    Encapsulates logic that replicates changes acquired from DAP API in a SQL database.
    """

    _session: DAPSession
    _connection: DatabaseConnection

    def __init__(self, session: DAPSession, connection: DatabaseConnection) -> None:
        self._session = session
        self._connection = connection

    async def initialize(
        self,
        namespace: str,
        table_name: str,
    ) -> None:
        """
        Initializes the given database table.
        """

        validator: AbstractDatabaseValidator = (
            self._connection.get_plugin().create_database_validator(
                namespace, table_name
            )
        )
        await validator.validate_init()

        client = await SnapshotClientFactory(
            self._session,
            namespace,
            table_name,
            self._connection.get_plugin().get_snapshot_query(),
        ).get_client()

        processor: AbstractProcessor = (
            self._connection.get_plugin().create_init_processor(
                namespace,
                table_name,
                client.table_schema,
            )
        )

        async with self._connection.get_plugin().get_connection().lock():
            await processor.prepare()

        metatable_manager: AbstractMetaTableManager = (
            self._connection.get_plugin().create_metatable_manager(
                namespace,
                table_name,
            )
        )

        async with self._connection.get_plugin().get_connection().lock():
            await metatable_manager.initialize(
                table_schema=client.table_schema, table_data=client.table_data
            )

        await client.download(
            self._connection.get_plugin().get_connection().lock, processor
        )

        async with self._connection.get_plugin().get_connection().lock():
            await self._connection.get_plugin().get_connection().commit()

    async def synchronize(
        self,
        namespace: str,
        table_name: str,
    ) -> None:
        """
        Synchronizes the given database table.
        """

        metatable_manager: AbstractMetaTableManager = (
            self._connection.get_plugin().create_metatable_manager(
                namespace,
                table_name,
            )
        )

        validator: AbstractDatabaseValidator = (
            self._connection.get_plugin().create_database_validator(
                namespace, table_name
            )
        )
        await validator.validate_sync()

        async with self._connection.get_plugin().get_connection().lock():
            since = await metatable_manager.get_timestamp()

        client = await IncrementalClientFactory(
            self._session,
            namespace,
            table_name,
            since,
            self._connection.get_plugin().get_incremental_query(),
        ).get_client()

        processor: AbstractProcessor = (
            self._connection.get_plugin().create_sync_processor(
                namespace,
                table_name,
                client.table_schema,
            )
        )

        async with self._connection.get_plugin().get_connection().lock():
            await processor.prepare()
            await metatable_manager.synchronize(client.table_schema, client.table_data)

        await client.download(
            self._connection.get_plugin().get_connection().lock, processor
        )

        async with self._connection.get_plugin().get_connection().lock():
            await self._connection.get_plugin().get_connection().commit()


class SQLDrop:
    """
    Encapsulates logic that drops a table from the SQL database.
    """

    _connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    async def drop(
        self,
        namespace: str,
        table_name: str,
    ) -> None:
        """
        Drops the given database table.
        """

        metatable_manager: AbstractMetaTableManager = (
            self._connection.get_plugin().create_metatable_manager(
                namespace,
                table_name,
            )
        )
        async with self._connection.get_plugin().get_connection().lock():
            await metatable_manager.drop()
            await self._connection.get_plugin().get_connection().commit()
