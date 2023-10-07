from ..integration.database import DatabaseConnection
from ..replicator.sql import SQLDrop


async def drop_db(connection_string: str, namespace: str, table_name: str) -> None:
    async with DatabaseConnection(connection_string).open() as db_connection:
        await SQLDrop(db_connection).drop(namespace, table_name)
