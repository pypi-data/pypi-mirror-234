from ..integration.plugin import register_database_plugin_type
from .mysql.mysql_plugin import MysqlPlugin
from .postgres.plugin import PostgresPlugin


def load() -> None:
    register_database_plugin_type("postgresql", PostgresPlugin)
    register_database_plugin_type("mysql", MysqlPlugin)
