from com.phida.main.sparksession import spark, logger


def getProfile():
    """
        desc:
            A static function to know the Environment SSA is being used in

        args:
            N/A

        return:
            String - Returns 'Databricks' or 'Synapse' or None

        example:
            profile = getProfile()

        tip:
            N/A

        """
    profile = spark.conf.get("spark.app.name")
    if profile == "Databricks Shell":
        logger.info(f"phida_log: SSA Running in Databricks Profile")
        return "Databricks"
    elif profile == "SynapseEnvPy":
        logger.info(f"phida_log: SSA Running in Azure Synapse Profile")
        return "Synapse"
    else:
        return None
