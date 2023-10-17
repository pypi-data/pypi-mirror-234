from pyspark.sql.types import StructType, StructField, LongType, StringType

from com.phida.main.Operations import hiveDDL, hasColumn, dropColumns, schemaDiff, addDerivedColumns, \
    getDerivedColumnsList, schemaDataTypeDiff, buildColumnsDict, buildJoinCondition


def create_test_df(spark):
    data = [
        (1851640136, "A.1", "9/17/2020 2:32:13 AM"),
        (4506678044, "B.1", "1/9/2023 2:46:38 PM"),
        (3087508287, "B.1", "8/8/2023 9:31:17 AM"),
        (3087508287, "B.2", "9/9/2023 9:35:17 AM")
    ]
    schema = StructType([
        StructField("PARTIDA2A2", LongType(), False),  # Column 1: "PARTIDA2A2" of type long
        StructField("REVISION", StringType(), True),  # Column 2: "REVISION" of type string
        StructField("UPDATESTAMP", StringType(), True)  # Column 3: "UPDATESTAMP" of type string
    ])

    return spark.createDataFrame(data, schema)


# Define a test DataFrame (df2) with a different schema
def create_test_df2(spark):
    data = [
        (4, "David", "Engineer"),
        (5, "Eve", "Designer")
    ]
    schema = StructType([
        StructField("id", LongType(), False),
        StructField("name", StringType(), True),
        StructField("occupation", StringType(), True)
    ])
    return spark.createDataFrame(data, schema)


def test_hive_ddl(spark_session):
    # Create a test DataFrame
    test_df = create_test_df(spark_session)

    # Call the hiveDDL method
    ddl_result = hiveDDL(test_df)

    # Define the expected DDL string based on the test DataFrame's schema
    expected_ddl = "`PARTIDA2A2` bigint,`REVISION` string,`UPDATESTAMP` string"

    # Assert that the generated DDL matches the expected result
    assert ddl_result == expected_ddl


def test_has_column(spark_session):
    # Create a test DataFrame
    test_df = create_test_df(spark_session)

    # Test with an existing column
    existing_column = "REVISION"
    result_existing = hasColumn(test_df, existing_column)
    assert result_existing is True

    # Test with a non-existing column
    non_existing_column = "EMAIL"
    result_non_existing = hasColumn(test_df, non_existing_column)
    assert result_non_existing is False


def test_drop_columns_with_test_data(spark_session):
    test_df = create_test_df(spark_session)

    # Columns to drop
    columns_to_drop = ["REVISION", "EMAIL"]  # "EMAIL" does not exist in the DataFrame

    # Call dropColumns method to drop columns
    result_df = dropColumns(test_df, columns_to_drop)

    # Assert that the specified columns have been dropped
    assert not hasColumn(result_df, "REVISION")

    # Assert that other columns still exist
    assert hasColumn(result_df, "PARTIDA2A2")
    assert hasColumn(result_df, "UPDATESTAMP")

    # Assert that the DataFrame still contains the same number of rows
    assert result_df.count() == test_df.count()


# Define the unit test for schemaDiff
def test_schema_diff(spark_session):
    # Create test DataFrames (df1 and df2)
    df1 = create_test_df(spark_session)
    df2 = create_test_df2(spark_session)

    # Call schemaDiff method to get the difference
    result_df = schemaDiff(df1, df2)

    # Verify that the resulting DataFrame contains only columns present in df1 but not in df2
    expected_columns = ["PARTIDA2A2", "REVISION", "UPDATESTAMP"]
    assert set(result_df.columns) == set(expected_columns)

    # Verify that the DataFrame still contains the same number of rows as df1
    assert result_df.count() == df1.count()


def test_addDerivedColumns(spark_session):
    # Create a test DataFrame using your create_test_df function
    df = create_test_df(spark_session)

    # Define a list of column expressions to add
    col_expr_list = ["length(REVISION) as rev_length"]

    # Call the function to add derived columns
    df_out = addDerivedColumns(df, col_expr_list)

    # Check if the derived column exists in the resulting DataFrame
    assert "rev_length" in df_out.columns

    # Check if the derived column has the expected values
    assert df_out.select("rev_length").collect()[0][0] == 3


def test_getDerivedColumnsList():
    # Define a list of column expressions
    col_expr_list = ["length(REVISION) as rev_length", "count(*) as total_count"]

    # Call the function to get derived column names
    derived_columns = getDerivedColumnsList(col_expr_list)

    # Check if the derived column names are extracted correctly
    assert derived_columns == ["rev_length", "total_count"]


def test_schemaDataTypeDiff(spark_session):
    # Create two test DataFrames with matching schemas
    data1 = [
        (1851640136, "Alice"),
        (4506678044, "Bob")
    ]
    schema1 = StructType([
        StructField("PARTIDA2A2", LongType(), False),
        StructField("REVISION", StringType(), True)
    ])
    df1 = spark_session.createDataFrame(data1, schema1)

    data2 = [
        (1, "Alice"),
        (2, "Bob")
    ]
    schema2 = StructType([
        StructField("id", LongType(), False),
        StructField("name", StringType(), True)  # Matched data type to StringType
    ])
    df2 = spark_session.createDataFrame(data2, schema2)

    # Call the function to find mismatched columns
    mismatched_columns = schemaDataTypeDiff(df1, df2)

    # Check if the mismatched columns are correctly identified
    assert mismatched_columns == []


def test_buildColumnsDict(spark_session):
    # Create a test DataFrame using your create_test_df function
    df = create_test_df(spark_session)

    # Define a list of columns to drop
    drop_columns = ["REVISION"]

    # Call the function to build the columns dictionary
    columns_dict = buildColumnsDict(df, drop_columns)

    # Check if the columns dictionary is correctly built
    expected_dict = {"`PARTIDA2A2`": "s.`PARTIDA2A2`", "`UPDATESTAMP`": "s.`UPDATESTAMP`"}
    assert columns_dict == expected_dict


def test_buildJoinCondition():
    # Define a list of key columns
    key_cols_list = ["column1", "column2", "column3"]

    # Call the function to build the join condition
    join_condition = buildJoinCondition(key_cols_list)

    # Check if the join condition is correctly built
    expected_condition = "t.`column1` <=> s.`column1` AND t.`column2` <=> s.`column2` AND t.`column3` <=> s.`column3`"
    assert join_condition == expected_condition
