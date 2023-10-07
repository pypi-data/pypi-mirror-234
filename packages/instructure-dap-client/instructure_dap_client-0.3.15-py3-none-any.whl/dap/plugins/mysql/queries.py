from typing import Awaitable, Callable, Optional, TypeVar

import aiomysql
from dap.integration.database_errors import DatabaseConnectionError
from dap.plugins.sqlalchemy.queries import SqlAlchemyQuery
from sqlalchemy.ext.asyncio import AsyncConnection

TReturn = TypeVar("TReturn")


class AioMysqlQuery(SqlAlchemyQuery[TReturn]):
    _query_func: Callable[[aiomysql.Connection], Awaitable[TReturn]]

    def __init__(
        self, query_func: Callable[[aiomysql.Connection], Awaitable[TReturn]]
    ) -> None:
        self._query_func = query_func

    async def __call__(self, conn: AsyncConnection) -> TReturn:
        mysql_conn: Optional[aiomysql.Connection] = (
            await conn.get_raw_connection()
        ).driver_connection
        if mysql_conn is None:
            raise DatabaseConnectionError

        return await self._query_func(mysql_conn)
