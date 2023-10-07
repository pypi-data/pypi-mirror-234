import abc
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncConnection

TReturn = TypeVar("TReturn")


class SqlAlchemyQuery(abc.ABC, Generic[TReturn]):
    @abc.abstractmethod
    async def __call__(self, conn: AsyncConnection) -> TReturn:
        ...


class SqlAlchemySyncQuery(SqlAlchemyQuery[TReturn]):
    _query_func: Callable[[sqlalchemy.Connection], TReturn]

    def __init__(self, query_func: Callable[[sqlalchemy.Connection], TReturn]) -> None:
        self._query_func = query_func

    async def __call__(self, conn: AsyncConnection) -> TReturn:
        return await conn.run_sync(self._query_func)


class SqlAlchemyExecutableQuery(SqlAlchemyQuery[sqlalchemy.CursorResult[TReturn]]):
    _statement: Union[
        sqlalchemy.Executable, Callable[[AsyncConnection], sqlalchemy.Executable]
    ]
    _parameters: List[Dict[str, Any]]

    def __init__(
        self,
        statement: Union[
            sqlalchemy.Executable, Callable[[AsyncConnection], sqlalchemy.Executable]
        ],
        parameters: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self._parameters = parameters or []
        self._statement = statement

    async def __call__(self, conn: AsyncConnection) -> sqlalchemy.CursorResult[TReturn]:
        if callable(self._statement):
            return await conn.execute(self._statement(conn), self._parameters)
        else:
            return await conn.execute(self._statement, self._parameters)
