import logging
from typing import TYPE_CHECKING
from typing import Optional

from tecton_core import conf


if TYPE_CHECKING:
    from duckdb import DuckDBPyConnection
logger = logging.getLogger(__name__)


class DuckDBContext:
    """
    Singleton holder of DuckDB connection.
    """

    _current_context_instance = None
    _connection = None

    def __init__(self, connection: "DuckDBPyConnection", home_dir_override: Optional[str] = None) -> None:
        self._connection = connection
        # Needed to export to S3
        if home_dir_override:
            connection.sql(f"SET home_directory='{home_dir_override}'")
        connection.sql("INSTALL httpfs;")
        duckdb_memory_limit = conf.get_or_none("DUCKDB_MEMORY_LIMIT")
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"Setting duckdb memory limit to {duckdb_memory_limit}")
        connection.sql(f"SET memory_limit='{duckdb_memory_limit}'")
        num_duckdb_threads = conf.get_or_none("DUCKDB_NTHREADS")
        if num_duckdb_threads:
            connection.sql(f"SET threads TO {num_duckdb_threads};")
            if conf.get_bool("DUCKDB_DEBUG"):
                print(f"Setting duckdb threads to {num_duckdb_threads}")
        # This is a workaround for pypika not supporting the // (integer division) operator
        connection.sql("CREATE OR REPLACE MACRO _tecton_int_div(a, b) AS a // b")
        extension_repo = conf.get_or_none("DUCKDB_EXTENSION_REPO")
        if extension_repo:
            connection.sql(f"SET custom_extension_repository='{extension_repo}'")
            connection.sql("INSTALL tecton")
            connection.sql("LOAD tecton")

    def get_connection(self):
        return self._connection

    @classmethod
    def get_instance(cls, home_dir_override: Optional[str] = None) -> "DuckDBContext":
        """
        Get the singleton instance of DuckDBContext.
        """
        if cls._current_context_instance is None:
            import duckdb

            conn_config = {}
            if conf.get_or_none("DUCKDB_EXTENSION_REPO"):
                conn_config["allow_unsigned_extensions"] = "true"

            if conf.get_bool("DUCKDB_PERSIST_DB"):
                conn = duckdb.connect("duckdb.db", config=conn_config)
            else:
                conn = duckdb.connect(config=conn_config)

            cls._current_context_instance = cls(conn, home_dir_override)

        return cls._current_context_instance
