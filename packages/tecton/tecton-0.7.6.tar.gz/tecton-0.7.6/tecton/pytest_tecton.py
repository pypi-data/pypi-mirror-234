import pytest

from tecton import tecton_context
from tecton.framework import validation_mode
from tecton_core import conf
from tecton_spark.udf_jar import get_udf_jar_path


def pytest_configure():
    # Set validation mode to 'skip' in unit test mode.
    validation_mode.set_validation_mode(validation_mode.ValidationMode.SKIP.value)

    # Force function serialization in test mode so it's as representative to
    # what Tecton will run in materialization.
    conf.set("TECTON_FORCE_FUNCTION_SERIALIZATION", "true")


@pytest.fixture(scope="session")
def tecton_pytest_spark_session():
    try:
        from pyspark.sql import SparkSession
    except ImportError:
        pytest.fail("Cannot create a SparkSession if `pyspark` is not installed.")

    active_session = SparkSession.getActiveSession()
    if active_session:
        pytest.fail(
            f"Cannot create SparkSession `tecton_pytest_spark_session` when there is already an active session: {active_session.sparkContext.appName}"
        )

    try:
        spark = (
            SparkSession.builder.appName("tecton_pytest_spark_session")
            .config("spark.jars", get_udf_jar_path())
            # This short-circuit's Spark's attempt to auto-detect a hostname for the master address, which can lead to
            # errors on hosts with "unusual" hostnames that Spark believes are invalid.
            .config("spark.driver.host", "localhost")
            .config("spark.ui.enabled", "false")
            .config("spark.sql.session.timeZone", "UTC")
            .getOrCreate()
        )
    except Exception as e:
        # Unfortunately we can't do much better than parsing the error message since Spark raises `Exception` rather than a more specific type.
        if str(e) == "Java gateway process exited before sending its port number":
            pytest.fail(
                "Failed to start Java process for Spark, perhaps Java isn't installed or the 'JAVA_HOME' environment variable is not set?"
            )

        raise e

    try:
        tecton_context.set_tecton_spark_session(spark)
        yield spark
    finally:
        spark.stop()
