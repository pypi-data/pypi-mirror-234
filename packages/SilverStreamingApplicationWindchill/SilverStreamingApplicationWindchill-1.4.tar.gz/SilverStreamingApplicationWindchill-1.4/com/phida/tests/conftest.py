import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session():
    # Create a SparkSession for testing
    spark = SparkSession.builder.appName("unit-test").getOrCreate()
    yield spark
    # Tear down the SparkSession after testing
    spark.stop()
