import pytest

from com.phida.main.utils import convertToUnixPath, pathExists, convertStrToList


def test_convert_to_unix_path():
    dbfs_path = "dbfs:/tmp/target/table_path"
    unix_path = convertToUnixPath(dbfs_path)
    assert unix_path == "/dbfs/tmp/target/table_path"


@pytest.mark.skip
def test_path_exists_with_existing_table(spark_session):
    # Define a temporary DataFrame to simulate an existing table
    test_data = [(1, "Alice"), (2, "Bob")]
    df = spark_session.createDataFrame(test_data, ["id", "name"])
    df.createOrReplaceTempView("temp_table")

    spark_session.sql("SHOW TABLES")

    # Test with the path of the temporary table
    table_path = "temp_table"
    assert pathExists(table_path) is True

    # Drop the temporary table to clean up after the test
    spark_session.catalog.dropTempView("temp_table")


def test_path_exists_with_non_existing_table():
    # Test with the path of a non-existing table
    table_path = "non_existing_table"
    result = pathExists(table_path)

    assert result is False


def test_convert_str_to_list():
    input_string = "abc,efg,hij"
    separator = ","
    result = convertStrToList(input_string, separator)
    expected_result = ["abc", "efg", "hij"]
    assert result == expected_result
