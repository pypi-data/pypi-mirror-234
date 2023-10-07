import logging

from ..integration.database import DatabaseConnection
from .base import Arguments, CommandRegistrar

logger = logging.getLogger("dap")


class AbstractDbCommandRegistrar(CommandRegistrar):
    async def _before_execute(self, args: Arguments) -> None:
        logger.debug(f"Checking connection to {args.connection_string}")
        async with DatabaseConnection(args.connection_string).open():
            # simply open and close connection to check validity
            pass
