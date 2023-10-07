import asyncio
import errno
import logging
import sys

from .arguments import Arguments
from .commands.commands import (
    DapCommandRegistrar,
    IncrementalCommandRegistrar,
    ListCommandRegistrar,
    SchemaCommandRegistrar,
    SnapshotCommandRegistrar,
)
from .commands.commonargs import (
    BaseUrlArgumentRegistrar,
    HelpArgumentRegistrar,
    LogLevelArgumentRegistrar,
    OAuthCredentialsArgumentRegistrar,
)
from .commands.dbargs import DatabaseConnectionStringArgumentRegistrar
from .commands.dropdb_command import DropDBCommandRegistrar
from .commands.initdb_command import InitDBCommandRegistrar
from .commands.queryargs import (
    FormatArgumentRegistrar,
    NamespaceArgumentRegistrar,
    OutputDirectoryArgumentRegistrar,
    TableArgumentRegistrar,
)
from .commands.syncdb_command import SyncDBCommandRegistrar
from .commands.timestampargs import SinceArgumentRegistrar, UntilArgumentRegistrar
from .dap_error import OperationError
from .log import LevelFormatter

dapCommand = DapCommandRegistrar(
    arguments=[
        BaseUrlArgumentRegistrar(),
        OAuthCredentialsArgumentRegistrar(),
        LogLevelArgumentRegistrar(),
        HelpArgumentRegistrar(),
    ],
    subcommands=[
        # Definition of the 'snapshot' command
        SnapshotCommandRegistrar(
            [
                TableArgumentRegistrar(),
                FormatArgumentRegistrar(),
                OutputDirectoryArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
            ]
        ),
        # Definition of the 'incremental' command
        IncrementalCommandRegistrar(
            [
                TableArgumentRegistrar(),
                FormatArgumentRegistrar(),
                OutputDirectoryArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                SinceArgumentRegistrar(),
                UntilArgumentRegistrar(),
            ]
        ),
        # Definition of the 'list' command
        ListCommandRegistrar([NamespaceArgumentRegistrar()]),
        # Definition of the 'schema' command
        SchemaCommandRegistrar(
            [
                NamespaceArgumentRegistrar(),
                TableArgumentRegistrar(),
                OutputDirectoryArgumentRegistrar(),
            ]
        ),
        # Definition of the 'initdb' command
        InitDBCommandRegistrar(
            [
                TableArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                DatabaseConnectionStringArgumentRegistrar(),
            ]
        ),
        # Definition of the 'syncdb' command
        SyncDBCommandRegistrar(
            [
                TableArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                DatabaseConnectionStringArgumentRegistrar(),
            ]
        ),
        # Definition of the 'dropdb' command
        DropDBCommandRegistrar(
            [
                TableArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                DatabaseConnectionStringArgumentRegistrar(),
            ]
        ),
    ],
)


def main() -> None:
    parser = dapCommand.register()

    args = Arguments()
    if parser:
        parser.parse_args(namespace=args)

    logging.basicConfig(level=getattr(logging, args.loglevel.upper(), logging.INFO))
    logger = logging.getLogger("dap")
    logger.propagate = False
    handler = logging.StreamHandler()

    default_format = "%(asctime)s - %(levelname)s - %(message)s"
    debug_format = default_format + " (%(filename)s:%(lineno)d)"
    handler.setFormatter(
        LevelFormatter({logging.DEBUG: debug_format, logging.INFO: default_format})
    )
    if args.logfile:
        file_handler = logging.FileHandler(args.logfile, "a")
        file_handler.setFormatter(
            LevelFormatter({logging.DEBUG: debug_format, logging.INFO: default_format})
        )
        logger.addHandler(file_handler)
    logger.addHandler(handler)

    asyncio.run(dapCommand.execute(args))


def console_entry() -> None:
    logger = logging.getLogger("dap")

    # handle exceptions for production deployments
    try:
        main()
    except OperationError as e:
        logger.error(
            f"An exception occurred while executing the command: {e.message} ({e.uuid})"
        )
        logger.exception(e)
        sys.exit(errno.EIO)
    except NotImplementedError as e:
        logger.exception(e)
        sys.exit(errno.ENOSYS)
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        sys.exit(errno.ECANCELED)
    except Exception as e:
        logger.exception(e)
        sys.exit(errno.EIO)


if __name__ == "__main__":
    console_entry()
