from ..api import DAPClient
from ..dap_types import Credentials
from ..integration.database import DatabaseConnection
from ..replicator.sql import SQLReplicator


async def init_db(
    base_url: str,
    credentials: Credentials,
    connection_string: str,
    namespace: str,
    table_name: str,
) -> None:
    async with DatabaseConnection(connection_string).open() as db_connection:
        async with DAPClient(base_url, credentials) as session:
            await SQLReplicator(session, db_connection).initialize(
                namespace, table_name
            )
