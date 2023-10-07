import abc
from typing import AsyncIterator, Dict, List, Optional, Tuple

import orjson
from strong_typing.core import JsonType

from .processor import AbstractProcessor, ContextAwareObject

JsonRecord = Dict[str, Dict[str, JsonType]]
TsvRecord = Tuple[Optional[bytes], ...]


class JSONLRecordProcessor(AbstractProcessor):
    "Base class for processing incoming records from DAP API in JSONL format."

    async def process(
        self, obj: ContextAwareObject, records: AsyncIterator[bytes]
    ) -> None:
        await self.process_impl(obj, self._convert(records))

    @abc.abstractmethod
    async def process_impl(
        self, obj: ContextAwareObject, records: AsyncIterator[JsonRecord]
    ) -> None:
        ...

    async def _convert(
        self, records: AsyncIterator[bytes]
    ) -> AsyncIterator[JsonRecord]:
        async for record in records:
            yield orjson.loads(record)


class TSVRecordProcessor(AbstractProcessor):
    "Base class for processing incoming records from DAP API in TSV format."

    _col_identifiers: List[bytes]

    def __init__(
        self,
        all_columns: List[str],
        primary_key_columns: List[str],
    ) -> None:
        self._col_identifiers = []
        for col in all_columns:
            if col in primary_key_columns:
                self._col_identifiers.append(f"key.{col}".encode("utf-8"))
            else:
                self._col_identifiers.append(f"value.{col}".encode("utf-8"))

    async def process(
        self, obj: ContextAwareObject, records: AsyncIterator[bytes]
    ) -> None:
        await self.process_impl(obj, self._convert(records))

    @abc.abstractmethod
    async def process_impl(
        self, obj: ContextAwareObject, records: AsyncIterator[TsvRecord]
    ) -> None:
        ...

    async def _convert(self, records: AsyncIterator[bytes]) -> AsyncIterator[TsvRecord]:
        iterator = records.__aiter__()
        try:
            header = await iterator.__anext__()
            col_names = header.split(b"\t")
            col_indices = [
                col_names.index(col_name) for col_name in self._col_identifiers
            ]

            while True:
                record = await iterator.__anext__()
                columns = record.split(b"\t")
                reordered_columns = tuple(
                    (columns[col_index] if columns[col_index] != b"\\N" else None)
                    for col_index in col_indices
                )
                yield reordered_columns
        except StopAsyncIteration:
            return
