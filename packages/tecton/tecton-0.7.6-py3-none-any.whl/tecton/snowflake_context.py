import logging

from tecton._internals.errors import MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS
from tecton._internals.sdk_decorators import sdk_public_method
from tecton_core import conf
from tecton_core import errors


logger = logging.getLogger(__name__)


@sdk_public_method
def set_connection(connection) -> "SnowflakeContext":
    """
    Connect tecton to Snowflake.

    :param connection: The SnowflakeConnection object.
    :return: A SnowflakeContext object.
    """
    from snowflake.connector import SnowflakeConnection

    if not isinstance(connection, SnowflakeConnection):
        msg = "connection must be a SnowflakeConnection object"
        raise errors.TectonValidationError(msg)

    return SnowflakeContext.set_connection(connection)


class SnowflakeContext:
    """
    Get access to Snowflake connection and session.
    """

    _current_context_instance = None
    _session = None
    _connection = None

    def __init__(self, connection):
        self._connection = connection
        if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
            from snowflake.snowpark import Session

            connection_parameters = {
                "connection": connection,
            }
            self._session = Session.builder.configs(connection_parameters).create()

    def get_session(self):
        if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
            if self._session is None:
                raise errors.SNOWFLAKE_CONNECTION_NOT_SET
            return self._session
        else:
            msg = "Snowflake session is only available with Snowpark enabled, use get_connection() instead"
            raise errors.TectonValidationError(msg)

    def get_connection(self):
        if self._connection is None:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET
        return self._connection

    @classmethod
    @sdk_public_method
    def get_instance(cls) -> "SnowflakeContext":
        """
        Get the singleton instance of SnowflakeContext.
        """
        # If the instance doesn't exist, raise the error to instruct user to set connection first. Otherwise
        # return the current snowflake context.
        if cls._current_context_instance is not None:
            return cls._current_context_instance
        else:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET

    @classmethod
    def set_connection(cls, connection) -> "SnowflakeContext":
        logger.debug("Generating new Snowflake session")
        # validate snowflake connection
        if not connection.database:
            msg = "database"
            raise MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)
        if not connection.warehouse:
            msg = "warehouse"
            raise MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)
        if not connection.schema:
            msg = "schema"
            raise MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)

        cls._current_context_instance = cls(connection)
        return cls._current_context_instance
