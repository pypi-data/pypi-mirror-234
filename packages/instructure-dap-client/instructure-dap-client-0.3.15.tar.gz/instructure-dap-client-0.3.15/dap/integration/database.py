import os
import re
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from .database_errors import DatabaseConnectionError
from .plugin import DatabasePlugin, create_database_plugin


class DatabaseConnection:
    _connection_string: str
    _database_plugin: DatabasePlugin
    _opened: bool

    def __init__(self, connection_string: Optional[str] = None) -> None:
        if connection_string is None:
            connection_string = os.getenv("DAP_CONNECTION_STRING")
            if not connection_string:
                raise DatabaseConnectionError("missing database connection string")
        self._connection_string = connection_string
        self._database_plugin = get_db_plugin_from_conn_string(connection_string)
        self._opened = False

    @asynccontextmanager
    async def open(self) -> AsyncIterator["DatabaseConnection"]:
        if self._opened:
            raise DatabaseConnectionError(f"database connection already opened")

        try:
            self._database_plugin.connect(self._connection_string)
            self._opened = True
            async with self._database_plugin.get_connection():
                yield self
        finally:
            await self._database_plugin.disconnect()
            self._opened = False

    def get_plugin(self) -> DatabasePlugin:
        return self._database_plugin


def get_db_plugin_from_conn_string(connection_string: str) -> DatabasePlugin:
    matches = re.findall(r"^([-\w]+)://.*$", connection_string)
    if len(matches) != 1:
        raise DatabaseConnectionError(
            f"wrong connection string format (accepted: 'dialect://address', actual: {connection_string})"
        )
    dialect = matches[0]
    database_plugin: Optional[DatabasePlugin] = create_database_plugin(dialect)
    if not database_plugin:
        raise DatabaseConnectionError(
            f"cannot find database plugin for dialect '{dialect}'"
        )
    return database_plugin
