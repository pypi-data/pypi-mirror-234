from com.phida.main.profileConfig import getProfile


def getTableProps():
    """
    desc:
        A static function to get the delta table properties to be used for table read and write
    args:
        N/A
    return:
        String - Returns string containing table props depending on what profile is returned
    example:
        tblProps = getTableProps()
    tip:
        N/A
    """
    if getProfile() == "Databricks":
        tblProps = "delta.autoOptimize.autoCompact = false, \n\
                     delta.autoOptimize.optimizeWrite = true, \n\
                     delta.tuneFileSizesForRewrites = true, \n\
                     delta.dataSkippingNumIndexedCols = 10, \n\
                     delta.enableChangeDataCapture = true"
    elif getProfile() == "Synapse":
        tblProps = "delta.autoOptimize.autoCompact = false, \n\
                             delta.autoOptimize.optimizeWrite = true, \n\
                             delta.dataSkippingNumIndexedCols = 10, \n\
                             delta.enableChangeDataCapture = true"
    return tblProps
