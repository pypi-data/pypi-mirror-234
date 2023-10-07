import abc
from typing import Dict, Optional, Type, TypeVar

from ..dap_types import TableQuery, VersionedSchema
from .connection import AbstractDatabaseConnection
from .meta_table import AbstractMetaTableManager
from .processor import AbstractProcessor
from .validator import AbstractDatabaseValidator


class DatabasePlugin(abc.ABC):
    """
    Interface of database plugin implementations.
    """

    @abc.abstractmethod
    def connect(self, connection_string: str) -> None:
        "Connects to the database specified in the given connection string."
        ...

    @abc.abstractmethod
    def get_connection(self) -> AbstractDatabaseConnection:
        "Gets the underlying database connection."
        ...

    @abc.abstractmethod
    def create_metatable_manager(
        self, namespace: str, table: str
    ) -> AbstractMetaTableManager:
        "Creates a metatable manager implementation."
        ...

    @abc.abstractmethod
    def create_init_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractProcessor:
        "Creates an init processor implementation."
        ...

    @abc.abstractmethod
    def create_sync_processor(
        self,
        namespace: str,
        table: str,
        schema: VersionedSchema,
    ) -> AbstractProcessor:
        "Creates a sync processor implementation."
        ...

    @abc.abstractmethod
    def create_database_validator(
        self,
        namespace: str,
        table: str,
    ) -> AbstractDatabaseValidator:
        "Creates a database validator."
        ...

    @abc.abstractmethod
    def get_snapshot_query(self) -> TableQuery:
        "Gets the query to be used for snapshot queries."
        ...

    @abc.abstractmethod
    def get_incremental_query(self) -> TableQuery:
        "Gets the query to be used for incremental queries."
        ...

    async def disconnect(self) -> None:
        "Disconnects from the database. Required by some database plugins."
        pass

    def get_table_name(self, namespace: str, table: str) -> str:
        """
        Gets the table name to be used in the database.
        Some plugins may require a different table name e.g. to include the namespace as prefix.

        :param namespace: the namespace name
        :param table: the table name
        :return: the table name to be used
        """
        return table


TPlugin = TypeVar("TPlugin", bound=DatabasePlugin)

_database_plugin_types: Dict[str, Type] = {}


def register_database_plugin_type(dialect: str, plugin_type: Type[TPlugin]) -> None:
    """
    Registers the given database plugin type for the given dialect. If a database plugin type is already
    registered for that dialect then this registration will be overriden.
    """
    _database_plugin_types[dialect] = plugin_type


def create_database_plugin(dialect: str) -> Optional[DatabasePlugin]:
    """
    Gets a database plugin instance of the type registered for the given dialect. If there is no database plugin type registered
    for the given dialect then None will be returned.
    """
    plugin_type: Optional[Type] = _database_plugin_types.get(dialect)
    return plugin_type() if plugin_type is not None else None


def has_database_plugin_type(dialect: str) -> bool:
    """
    Checks whether a database plugin type has been registered for the given dialect.
    """
    return dialect in _database_plugin_types


def unregister_database_plugin_type(dialect: str) -> None:
    """
    Unregisters the database plugin type that is registered for the given dialect. If there is no database
    plugin type registered for the given dialect then this function has no effect.
    """
    _database_plugin_types.pop(dialect, None)


def unregister_all_database_plugin_types() -> None:
    """
    Unregisters all previously registered database plugin types.
    """
    _database_plugin_types.clear()
