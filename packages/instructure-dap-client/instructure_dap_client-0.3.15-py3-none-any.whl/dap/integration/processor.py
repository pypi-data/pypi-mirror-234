import abc
from dataclasses import dataclass
from typing import AsyncIterator

from ..dap_types import JobID, ObjectID


@dataclass(frozen=True)
class ContextAwareObject:
    "Provides information about the context in which the records are processed."

    id: ObjectID
    index: int
    total_count: int
    job_id: JobID

    def __str__(self) -> str:
        return f"[object {self.index + 1}/{self.total_count} - job {self.job_id}]"


class AbstractProcessor(abc.ABC):
    @abc.abstractmethod
    async def prepare(self) -> None:
        """
        Prepares for processing of a stream of records.

        For initializing a database, this would issue SQL `CREATE TABLE` statements that records about to be received
        might be inserted into.

        """
        ...

    @abc.abstractmethod
    async def process(
        self, obj: ContextAwareObject, records: AsyncIterator[bytes]
    ) -> None:
        """
        Starts processing a batch of records from the given object.

        :param obj: Object that the records belong to. This helps trace records back to their source.
        :param records: The asynchronously iterable collection of records.
        """
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Ends processing records. Invoked after all records have been processed.
        """
        ...
