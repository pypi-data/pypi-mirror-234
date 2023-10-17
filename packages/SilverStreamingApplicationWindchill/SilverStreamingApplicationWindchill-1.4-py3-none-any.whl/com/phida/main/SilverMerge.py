from delta.tables import DeltaTable
from pyspark.sql.functions import row_number, col, to_timestamp
from pyspark.sql.window import Window

from com.phida.main.Operations import tableExists, addDerivedColumns, createDeltaTable, alterDeltaTable, \
    dropColumns, schemaDiff, getKeyCols, buildJoinCondition, buildColumnsDict, hiveDDL, \
    schemaDataTypeDiff, hasColumn
from com.phida.main.sparksession import spark, logger
from com.phida.main.utils import pathExists, convertStrToList


class SilverMerge:
    """
    A streaming pipeline for cleansing incremental data from Bronze table and merge into Silver

    args:
        srcDatabaseName: String - Source Database (typically Bronze)
        srcTableName: String - Source Table Name
        tgtDatabaseName: String - Target Database Name (Will be created if not exists)
        tgtTableName: String - Target Table Name (Will be created if not exists)
        tgtCheckpoint: String - Target Checkpoint (For storing the status of the stream)
        tgtTablePath: String - Target Table Path (so that the table is created as external)
        tgtPartitionColumns: String - Target partition columns (optional)
        derivedColExpr: String - Derived columns to be added to Silver, separated by § (optional)
        triggerOnce: String - Whether continuous streaming or just once
        dropColumnStr: String - Columns to be dropped from source table df
        pruneColumn: String - Column for applying the prune filter in the merge ON condition clause \
                              (to improve performance of the merge)

    methods:
        silverCleansing
        prepareTarget
        upsertToDelta
        streamIntoDeltaTarget

    example:
        from com.phida.SilverMerge import SilverMerge
        silverMergeObj = SilverMerge(srcDatabaseName, srcTableName, tgtDatabaseName, tgtTableName,
                 tgtCheckpoint, tgtTablePath, tgtPartitionColumns, derivedColExpr,
                 triggerOnce, dropColumnStr, pruneColumn)

    """

    def __init__(self, srcDatabaseName, srcTableName, tgtDatabaseName, tgtTableName,
                 tgtCheckpoint, tgtTablePath, tgtPartitionColumns, derivedColExpr,
                 triggerOnce, dropColumnStr, pruneColumn):
        """
        desc:
            Initialize the required class variables

        args:
            srcDatabaseName: String - Source Database (typically Bronze)
            srcTableName: String - Source Table Name
            tgtDatabaseName: String - Target Database Name (Will be created if not exists)
            tgtTableName: String - Target Table Name (Will be created if not exists)
            tgtCheckpoint: String - Target Checkpoint (For storing the status of the stream)
            tgtTablePath: String - Target Table Path (so that the table is created as external)
            tgtPartitionColumns: String - Target partition columns (optional)
            derivedColExpr: String - Derived columns to be added to Silver, separated by § (optional)
            triggerOnce: String - Whether continuous streaming or just once
            dropColumnStr: String - Columns to be dropped from source table df
            pruneColumn: String - Column to use for dynamic file pruning (future feature)

        """

        logger.info("phida_log: Initialising class variables")

        self.srcDatabaseName = srcDatabaseName
        self.srcTableName = srcTableName
        self.tgtDatabaseName = tgtDatabaseName
        self.tgtTableName = tgtTableName
        self.tgtCheckpoint = tgtCheckpoint
        self.tgtTablePath = tgtTablePath
        self.tgtPartitionColumns = tgtPartitionColumns
        self.derivedColExpr = derivedColExpr
        self.triggerOnce = triggerOnce
        self.dropColumnStr = dropColumnStr
        self.pruneColumn = pruneColumn

        logger.info(f"phida_log: Check if source table {self.srcDatabaseName}.{self.srcTableName} exists")

        if tableExists(self.srcDatabaseName, self.srcTableName):
            logger.info(f"phida_log: source table exists")

            logger.info(f"phida_log: initialising derived class variables")

            self.srcDF = spark.readStream.table(self.srcDatabaseName + "." + self.srcTableName)

            self.isDataSourceHVR = hasColumn(self.srcDF, "hvr_integ_key")

            self.keyCols = getKeyCols(self.srcDatabaseName, self.srcTableName)

            self.keyColsList = convertStrToList(self.keyCols, ",")

            self.joinCondition = buildJoinCondition(self.keyColsList)

            self.condition = f"{self.pruneColumn} <> '' AND {self.joinCondition}" if self.pruneColumn.strip() \
                else self.joinCondition

            self.dropColumnList = convertStrToList(self.dropColumnStr, ",")

            self.columnsDict = buildColumnsDict(self.srcDF, self.dropColumnList)

    def silverCleansing(self):
        """
        desc:
            A Method for reading from source table (Bronze) as a stream and apply cleansing transformations

        args:
            None

        return:
            silverCleansedDF: DataFrame - returns the bronze dataframe after cleansing

        example:
            silverCleansing()

        tip:
            N/A
        """
        logger.info(f"phida_log: applying cleansing rules on source dataframe ")

        if tableExists(self.srcDatabaseName, self.srcTableName):

            silverRawDF = self.srcDF

            if self.derivedColExpr:
                derivedColExprList = convertStrToList(self.derivedColExpr, "§")

                silverDerivedColumns = addDerivedColumns(silverRawDF, derivedColExprList)

            else:
                silverDerivedColumns = silverRawDF

            self.columnsDict = buildColumnsDict(silverDerivedColumns, self.dropColumnList)

            return silverDerivedColumns

    def prepareTarget(self, inDF):
        """
        desc:
            A Method for preparing the target delta table.
            Creates the delta table if it does not exists
            Raise error if there are missing column(s) 
            Raise error if data types are different between existing table and source table
            Alters the delta table if there is new column added in the source schema

        args:
            inDF: DataFrame - input spark dataframe (typically the output of silverCleansing())

        return:
            None - Does not return anything - Just creates or alters the target delta table

        example:
            prepareTarget(silverCleansedDF)

        tip:
            N/A
        """
        logger.info(f"phida_log: preparing the target delta table ")

        targetTableExists = tableExists(self.tgtDatabaseName, self.tgtTableName)

        targetPathExists = pathExists(self.tgtTablePath)

        inDF = dropColumns(inDF, self.dropColumnList)

        first_run = False if (targetTableExists & targetPathExists) else True

        if first_run:

            logger.info(f"phida_log: This seems to be the first run")
            logger.info(f"phida_log: creating the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            createDeltaTable(inDF,
                             self.tgtTablePath,
                             self.tgtDatabaseName,
                             self.tgtTableName,
                             self.tgtPartitionColumns)

        else:

            existingDF = spark.read.table(self.tgtDatabaseName + "." + self.tgtTableName)

            diff2DF = schemaDiff(existingDF, inDF)

            if diff2DF.columns:
                raise Exception(f"Column(s) {diff2DF.columns} is(are) missing")

            mismatched_columns = schemaDataTypeDiff(existingDF, inDF)

            if mismatched_columns:
                raise Exception(f"There is data type mismatch in column(s): {mismatched_columns}")

            diffDF = schemaDiff(inDF, existingDF)

            addColumns = hiveDDL(diffDF)

            if addColumns:
                logger.info(f"phida_log: There seems to be a schema change in silver")
                logger.info(f"phida_log: Altering the target table {self.tgtDatabaseName}.{self.tgtTableName}")

                alterDeltaTable(self.tgtDatabaseName, self.tgtTableName, addColumns)

                logger.info(f"phida_log: newly added columns {addColumns}")

            else:
                logger.info(f"phida_log: There is no change in schema in silver")

    def upsertToDelta(self, microBatchOutputDF, batchId):
        """
        desc:
            A Function for merging the records from a given dataframe into delta Target table (foreachBatch)

        args:
            microBatchOutputDF: DataFrame -
            batchId: BigInt - required by the foreachBatch stream processor

        return:
            None - Does not return anything - This function is used by foreachbatch in streamIntoDeltaTarget

        example:
            N/A - see method streamIntoDeltaTarget() for usage

        tip:
            N/A
        """

        microBatchOutputDF = microBatchOutputDF.filter("source_operation in (0,1,2,3)")

        if self.isDataSourceHVR:
            windowSpec = Window.partitionBy(self.keyColsList) \
                .orderBy(col("src_commit_time").desc(), col("hvr_integ_key").desc())
        else:
            windowSpec = Window.partitionBy(self.keyColsList) \
                .orderBy(to_timestamp(col("UPDATESTAMP"), "M/d/yyyy h:mm:ss a").desc())

        microBatchOutputDF = microBatchOutputDF.withColumn("latest_record", row_number().over(windowSpec)) \
            .filter("latest_record == 1").drop("latest_record")

        tgtDeltaTable = DeltaTable.forName(spark, self.tgtDatabaseName + "." + self.tgtTableName)

        tgtDeltaTable.alias("t").merge(microBatchOutputDF.alias("s"), self.condition) \
            .whenMatchedDelete("s.source_operation in (0,3)") \
            .whenMatchedUpdate(condition="s.source_operation not in (0,3)", set=self.columnsDict) \
            .whenNotMatchedInsert(condition="s.source_operation not in (0,3)", values=self.columnsDict) \
            .execute()

    def streamIntoDeltaTarget(self):
        """
        desc:
            A Function for writing the given streaming dataframe into Delta Target table with foreachBatch merge
            Main layer the triggers/kicks off the entire process of reading from Bronze and merging into silver.
        args:
            None

        return:
            outputDF: DataFrame - Returns a spark streaming dataframe that writes into target delta table

        example:
            streamIntoDeltaTarget()

        tip:
            N/A
        """

        silverCleansedDF = self.silverCleansing()

        self.prepareTarget(silverCleansedDF)

        logger.info(f"phida_log: performing streaming merge on target {self.tgtDatabaseName}.{self.tgtTableName}")

        if self.triggerOnce == "Y":
            outputDF = (silverCleansedDF.writeStream
                        .outputMode("update")
                        .option("checkpointLocation", self.tgtCheckpoint)
                        .option("failOnDataLoss", False)
                        .trigger(once=True)
                        .queryName(self.srcDatabaseName + "_" + self.srcTableName + "_to_" +
                                   self.tgtDatabaseName + "_" + self.tgtTableName)
                        .foreachBatch(self.upsertToDelta)
                        .start(self.tgtTablePath)
                        )
        else:
            outputDF = (silverCleansedDF.writeStream
                        .outputMode("update")
                        .option("checkpointLocation", self.tgtCheckpoint)
                        .option("failOnDataLoss", False)
                        .queryName(self.srcDatabaseName + "_" + self.srcTableName + "_to_" +
                                   self.tgtDatabaseName + "_" + self.tgtTableName)
                        .foreachBatch(self.upsertToDelta)
                        .start(self.tgtTablePath)
                        )

        return outputDF
