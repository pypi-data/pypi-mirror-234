import abc

class AbstractDatabaseValidator(abc.ABC):
    """ 
    Interface for validating local database
    """
    @abc.abstractmethod
    async def validate_init(self) -> None:
        """
        Validates the local database before an init operation
        """
        ...

    @abc.abstractmethod
    async def validate_sync(self) -> None:
        """
        Validates the local database before a sync operation
        """
        ...
