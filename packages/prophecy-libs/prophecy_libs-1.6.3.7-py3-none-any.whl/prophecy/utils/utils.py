import json
import os
import zipfile
from typing import Optional

from pyspark.sql import *

from prophecy.libs.utils import *


class ProphecyDataFrame:
    def __init__(self, df: DataFrame, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.spark = spark
        self.sqlContext = SQLContext(spark.sparkContext, sparkSession=spark)

        if type(df) == DataFrame:
            try:  # for backward compatibility
                self.extended_dataframe = (
                    self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(
                        df._jdf
                    )
                )
            except TypeError:
                self.extended_dataframe = (
                    self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
                )
            self.dataframe = df
        else:
            try:
                self.extended_dataframe = (
                    self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(
                        df._jdf
                    )
                )
            except TypeError:
                self.extended_dataframe = (
                    self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
                )
            self.dataframe = DataFrame(df, self.sqlContext)

    def interim(
            self,
            subgraph,
            component,
            port,
            subPath,
            numRows,
            interimOutput,
            detailedStats=False,
    ) -> DataFrame:
        result = self.extended_dataframe.interim(
            subgraph, component, port, subPath, numRows, interimOutput, detailedStats
        )
        return DataFrame(result, self.sqlContext)

    # Ab Initio extensions to Prophecy DataFrame
    def collectDataFrameColumnsToApplyFilter(
            self,
            columnList,
            filterSourceDataFrame
    ) -> DataFrame:
        result = self.extended_dataframe.collectDataFrameColumnsToApplyFilter(
            createScalaList(self.spark, columnList), filterSourceDataFrame._jdf
        )
        return DataFrame(result, self.sqlContext)

    def normalize(
            self,
            lengthExpression,
            finishedExpression,
            finishedCondition,
            alias,
            colsToSelect,
            tempWindowExpr,
            lengthRelatedGlobalExpressions={}
    ) -> DataFrame:
        result = self.extended_dataframe.normalize(
            createScalaColumnOption(self.spark, lengthExpression),
            createScalaColumnOption(self.spark, finishedExpression),
            createScalaColumnOption(self.spark, finishedCondition),
            alias,
            createScalaColumnList(self.spark, colsToSelect),
            createScalaColumnMap(self.spark, tempWindowExpr),
            createScalaColumnMap(self.spark, lengthRelatedGlobalExpressions)
        )
        return DataFrame(result, self.sqlContext)

    def denormalizeSorted(
            self,
            groupByColumns,
            orderByColumns,
            denormalizeRecordExpression,
            finalizeExpressionMap,
            inputFilter,
            outputFilter,
            denormColumnName,
            countColumnName="count") -> DataFrame:
        result = self.extended_dataframe.denormalizeSorted(
            self,
            createScalaColumnList(self.spark, groupByColumns),
            createScalaColumnList(self.spark, orderByColumns),
            denormalizeRecordExpression,
            createScalaColumnMap(self.spark, finalizeExpressionMap),
            createScalaColumnOption(self.spark, inputFilter),
            createScalaColumnOption(self.spark, outputFilter),
            denormColumnName,
            countColumnName)
        return DataFrame(result, self.sqlContext)

    def readSeparatedValues(
            self,
            inputColumn,
            outputSchemaColumns,
            recordSeparator,
            fieldSeparator
    ) -> DataFrame:
        result = self.extended_dataframe.readSeparatedValues(
            inputColumn._jc,
            createScalaList(self.spark, outputSchemaColumns),
            recordSeparator,
            fieldSeparator
        )
        return DataFrame(result, self.sqlContext)

    def syncDataFrameColumnsWithSchema(self, columnNames) -> DataFrame:
        result = self.extended_dataframe.syncDataFrameColumnsWithSchema(createScalaList(self.spark, columnNames))
        return DataFrame(result, self.sqlContext)

    def zipWithIndex(
            self,
            startValue,
            incrementBy,
            indexColName,
            sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.zipWithIndex(startValue,
                                                      incrementBy,
                                                      indexColName,
                                                      sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def metaPivot(
            self,
            pivotColumns,
            nameField,
            valueField,
            sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.metaPivot(pivotColumns,
                                                   nameField,
                                                   valueField,
                                                   sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def compareRecords(self, otherDataFrame, componentName, limit, sparkSession) -> DataFrame:
        result = self.extended_dataframe.compareRecords(otherDataFrame._jdf,
                                                        componentName,
                                                        limit,
                                                        sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def generateSurrogateKeys(
            self,
            keyDF,
            naturalKeys,
            surrogateKey,
            overrideSurrogateKeys,
            computeOldPortOutput,
            spark
    ) -> (DataFrame, DataFrame, DataFrame):
        result = self.extended_dataframe.generateSurrogateKeys(
            keyDF._jdf,
            createScalaList(self.spark, naturalKeys),
            surrogateKey,
            createScalaOption(self.spark, overrideSurrogateKeys),
            computeOldPortOutput,
            spark._jsparkSession)
        result.toString()
        return (DataFrame(result._1(), self.sqlContext), DataFrame(result._2(), self.sqlContext),
                DataFrame(result._3(), self.sqlContext))

    def generateLogOutput(
            self,
            componentName,
            subComponentName,
            perRowEventTypes,
            perRowEventTexts,
            inputRowCount,
            outputRowCount,
            finalLogEventType,
            finalLogEventText,
            finalEventExtraColumnMap,
            sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.generateLogOutput(
            componentName,
            subComponentName,
            createScalaColumnOption(self.spark, perRowEventTypes),
            createScalaColumnOption(self.spark, perRowEventTexts),
            inputRowCount,
            createScalaOption(self.spark, outputRowCount),
            createScalaColumnOption(self.spark, finalLogEventType),
            createScalaColumnOption(self.spark, finalLogEventText),
            createScalaColumnMap(self.spark, finalEventExtraColumnMap),
            sparkSession._jsparkSession
        )

        return DataFrame(result, self.sqlContext)

    def mergeMultipleFileContentInDataFrame(
            self,
            fileNameDF,
            spark,
            delimiter,
            readFormat,
            joinWithInputDataframe,
            outputSchema=None,
            ffSchema=None,
            abinitioSchema=None
    ) -> DataFrame:
        if outputSchema is not None:
            result = self.extended_dataframe.mergeMultipleFileContentInDataFrame(
                fileNameDF._jdf,
                spark._jsparkSession,
                outputSchema.json(),
                delimiter,
                readFormat,
                joinWithInputDataframe,
                createScalaOption(self.spark, ffSchema)
            )
        else:
            result = self.extended_dataframe.mergeMultipleFileContentInDataFrame(
                fileNameDF._jdf,
                spark._jsparkSession,
                abinitioSchema,
                delimiter,
                readFormat,
                joinWithInputDataframe
            )
        return DataFrame(result, self.sqlContext)

    def breakAndWriteDataFrameForOutputFile(
            self,
            outputColumns,
            fileColumnName,
            format,
            delimiter
    ) -> DataFrame:
        result = self.extended_dataframe.breakAndWriteDataFrameForOutputFile(
            createScalaList(self.spark, outputColumns),
            fileColumnName,
            format,
            self.createScalaOption(delimiter))
        return DataFrame(result, self.sqlContext)

    def __getattr__(self, item: str):
        if item == "interim":
            self.interim

        if hasattr(self.extended_dataframe, item):
            return getattr(self.extended_dataframe, item)
        else:
            return getattr(self.dataframe, item)


class InterimConfig:
    def __init__(self):
        self.isInitialized = False
        self.interimOutput = None

    def initialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        self.isInitialized = True
        self.interimOutput = (
            spark.sparkContext._jvm.org.apache.spark.sql.InterimOutputHive2.apply(
                sessionForInteractive
            )
        )

    def maybeInitialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        if not self.isInitialized:
            self.initialize(spark, sessionForInteractive)

    def clear(self):
        self.isInitialized = False
        self.interimOutput = None


interimConfig = InterimConfig()


class ProphecyDebugger:

    @classmethod
    def is_prophecy_wheel(cls, path):
        import zipfile
        zip = zipfile.ZipFile(path)
        for name in zip.namelist():
            if "workflow.latest.json" in name:
                return True
        return False

    @classmethod
    def wheels_in_path(cls):
        import sys, pathlib
        l = []
        for p in sys.path:
            try:
                for child in pathlib.Path(p).rglob("*.whl"):
                    if ProphecyDebugger.is_prophecy_wheel(child):
                        l.append(str(child))
            except IOError as e:
                ProphecyDebugger.log(None, f"Error when trying to read path {p}: {str(e)}")
                pass
        return l

    @classmethod
    def wheels_in_site_packages(cls):
        import sys
        target_file = 'direct_url.json'
        url_list = []
        # Get list of site-packages directories
        site_packages = [s for s in sys.path if "cluster_libraries" in s]

        # Walk through each site-packages directory
        for site_package in site_packages:
            for dirpath, dirnames, filenames in os.walk(site_package):
                if target_file in filenames:
                    # Construct full path to the target file
                    file_path = os.path.join(dirpath, target_file)
                    try:
                        # Open and read the target file
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            if 'url' in data:
                                url_list.append(data['url'].replace('file://', ''))
                    except Exception as e:
                        ProphecyDebugger.log(None, f"Error reading {file_path}: {e}")
        return url_list

    # Uses a different ijson library. Accurate, but adds another dependency to libs
    # @classmethod
    # def find_file_in_wheel(cls, filename, wheel_path, desired_value):
    #     try:
    #         with zipfile.ZipFile(wheel_path, 'r') as z:
    #             if filename in z.namelist():
    #                 with z.open(filename) as json_file:
    #                     parser = ijson.parse(json_file)
    #                     for prefix, event, value in parser:
    #                         if prefix == "a.b" and value == desired_value:
    #                             # Reset the file pointer to the beginning
    #                             json_file.seek(0)
    #                             # Read and return the entire content
    #                             return json_file.read().decode('utf-8')
    #     except zipfile.BadZipFile:
    #         print(f"Warning: Could not read {wheel_path}. Might be a corrupted wheel.")
    #     except PermissionError:
    #         print(f"Warning: Permission denied when trying to read {wheel_path}.")
    #     except IOError as e:
    #         print(f"Warning: IO Error ({e}) when trying to read {wheel_path}.")
    #     return None

    @classmethod
    def find_pipeline_json_in_wheel(cls, wheel_path, pipeline_uri, filename="workflow.latest.json"):
        key_pattern = f'"uri" : "{pipeline_uri}"'  # Basic pattern match to avoid using new dependencies
        try:
            with zipfile.ZipFile(wheel_path, 'r') as z:
                if any(name.endswith(filename) for name in z.namelist()):
                    for file_to_read in z.namelist():
                        with z.open(file_to_read) as json_file:
                            content = json_file.read().decode('utf-8')
                            if key_pattern in content:
                                return {name: z.read(name).decode('utf-8') for name in z.namelist() if
                                        not os.path.isdir(name)}
        except zipfile.BadZipFile:
            ProphecyDebugger.log(None, f"Warning: Could not read {wheel_path}. Might be a corrupted wheel.")
        except PermissionError:
            ProphecyDebugger.log(None, f"Warning: Permission denied when trying to read {wheel_path}.")
        except IOError as e:
            ProphecyDebugger.log(None, f"Warning: IO Error ({e}) when trying to read {wheel_path}.")
        return None

    @classmethod
    def find_current_pipeline_code_in_path(cls, pipeline_uri):
        for wheel_path in ProphecyDebugger.wheels_in_path() + ProphecyDebugger.wheels_in_site_packages():
            possible_content = ProphecyDebugger.find_pipeline_json_in_wheel(wheel_path, pipeline_uri)
            if possible_content:
                return possible_content
        ProphecyDebugger.log(None, f"Couldn't find pipeline code for pipeline {pipeline_uri}")
        return None

    @classmethod
    def log(cls, spark: SparkSession, s: str):
        import logging
        # log4jLogger = sc._jvm.org.apache.log4j
        # LOGGER = log4jLogger.LogManager.getLogger("ProphecyDebugger")
        # LOGGER.info(s)
        logger = logging.getLogger('py4j')
        logger.info(s)

    @classmethod
    def sparkSqlShow(cls, spark: SparkSession, query: str):
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkSqlShow(spark._jsparkSession, query)

    @classmethod
    def sparkSql(cls, spark: SparkSession, query: str):
        jdf = spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkSql(spark._jsparkSession, query)
        return DataFrame(jdf, spark)

    @classmethod
    def exception(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.exception(spark._jsparkSession)

    @classmethod
    def class_details(cls, spark: SparkSession, name: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.classDetails(spark._jsparkSession, name)

    @classmethod
    def spark_conf(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkConf(spark._jsparkSession)

    @classmethod
    def runtime_conf(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.runtimeConf(spark._jsparkSession)

    @classmethod
    def local_properties(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localProperties(spark._jsparkSession)

    @classmethod
    def local_property(cls, spark: SparkSession, key: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localProperty(spark._jsparkSession, key)

    @classmethod
    def local_property_async(cls, spark: SparkSession, key: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localPropertyAsync(spark._jsparkSession,
                                                                                                key)

    @classmethod
    def get_scala_object(cls, spark: SparkSession, className: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.getScalaObject(spark._jsparkSession,
                                                                                            className)

    @classmethod
    def call_scala_object_method(cls, spark: SparkSession, className: str, methodName: str, args: list = []):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.callScalaObjectMethod(
            spark._jsparkSession, className, methodName, args)

    @classmethod
    def call_scala_object_method_async(cls, spark: SparkSession, className: str, methodName: str, args: list = []):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.callScalaObjectMethodAsync(
            spark._jsparkSession, className, methodName, args)


class MetricsCollector:

    # Called only for interactive execution and metrics mode.
    @classmethod
    def initializeMetrics(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.initializeMetrics(
            spark._jsparkSession
        )

    # We don't have positional arguments in python code base, thereby moving directly to keyword based argument.
    @classmethod
    def start(
            cls, spark: SparkSession, sessionForInteractive: str = "", pipelineId: str = "", config=None, **kwargs
    ):
        global interimConfig
        interimConfig.maybeInitialize(spark, sessionForInteractive)

        # Define a function to convert object to a dictionary
        def should_include(key):
            ## these are in config objects but we need to remove them.
            return key not in ['spark', 'prophecy_spark']

        def to_dict_recursive(obj):
            if isinstance(obj, (list, tuple)):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: to_dict_recursive(value) for key, value in obj.items() if should_include(key)}
            elif hasattr(obj, '__dict__'):
                return to_dict_recursive({key: value for key, value in obj.__dict__.items() if should_include(key)})
            elif hasattr(obj, '__slots__'):
                return to_dict_recursive(
                    {slot: getattr(obj, slot) for slot in obj.__slots__ if should_include(slot)})
            else:
                return obj

        for key, value in kwargs.items():
            ProphecyDebugger.log(None, f"Unused argument passed -- key: {key}, value: {value}")

        pipeline_code = ProphecyDebugger.find_current_pipeline_code_in_path(pipeline_uri=pipelineId)
        # if isBlank(sessionForInteractive):  # when running as job
        #     # if not set by the user, try to set it automatically
        #     if not spark.conf.get("spark.prophecy.packages", None):
        #         wheels = ProphecyDebugger.wheels_in_path()
        #         str1 = ",".join(wheels)
        #         spark.conf.set("spark.prophecy.packages", str1)
        #         ProphecyDebugger.log(spark, "wheels " + str1)
        if config is not None:
            pipeline_config = json.dumps(config, default=to_dict_recursive, indent=4)
            try:
                if pipeline_code is None:
                    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
                        spark._jsparkSession, pipelineId, sessionForInteractive, pipeline_config
                    )
                else:
                    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
                        spark._jsparkSession, pipelineId, sessionForInteractive, pipeline_config, pipeline_code
                    )
            except Exception as ex:
                print("Exception while starting metrics collector: ", ex)
                raise ex

        else:
            if not isBlank(sessionForInteractive) or pipeline_code is None:
                # Not passing pipeline code for interactive runs
                spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
                    spark._jsparkSession, pipelineId, sessionForInteractive
                )
            else:
                spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
                    spark._jsparkSession, pipelineId, sessionForInteractive, pipeline_code
                )

    @classmethod
    def end(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.end(
            spark._jsparkSession
        )
        global interimConfig
        interimConfig.clear()


def collectMetrics(
        spark: SparkSession,
        df: DataFrame,
        subgraph: str,
        component: str,
        port: str,
        numRows: int = 40,
) -> DataFrame:
    global interimConfig
    interimConfig.maybeInitialize(spark)
    pdf = ProphecyDataFrame(df, spark)
    return pdf.interim(
        subgraph, component, port, "dummy", numRows, interimConfig.interimOutput
    )


def createEventSendingListener(
        spark: SparkSession, execution_url: str, session: str, scheduled: bool
):
    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.addSparkListener(
        spark._jsparkSession, execution_url, session, scheduled)


def postDataToSplunk(props: dict, payload):
    import gzip
    import requests
    from requests import HTTPError
    from requests.adapters import HTTPAdapter
    from urllib3 import Retry

    with requests.Session() as session:
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=int(props.get("maxRetries", 4)),
                backoff_factor=float(props.get("backoffFactor", 1)),
                status_forcelist=[429, 500, 502, 503, 504],
            )
        )
        session.mount("http://", adapter)
        session.headers.update(
            {
                "Authorization": "Splunk " + props["token"],
                "Content-Encoding": "gzip",
                "BatchId": props.get("batchId", None),
            }
        )
        res = session.post(
            props["url"], gzip.compress(bytes(payload, encoding="utf8"))
        )
        print(f"IN SESSION URL={props['url']} res.status_code = {res.status_code} res={res.text}")
        if res.status_code != 200 and props.get("stopOnFailure", False):
            raise HTTPError(res.reason)


def splunkHECForEachWriter(props: dict):
    def wrapper(batchDF: DataFrame, batchId: int):
        max_load: Optional[int] = props.get("maxPayload")
        # Take 90% of the payload limit and convert KB into Bytes
        max_load = int(0.9 * 1024 * int(max_load)) if max_load else None
        props.update({"batchId": str(batchId)})

        def f(iterableDF):
            payload, prevsize = "", 0

            for row in iterableDF:
                if max_load and prevsize + len(row) >= max_load:
                    print(f"buffer hit at size {prevsize}")
                    postDataToSplunk(props, payload)
                    payload, prevsize = "", 0
                else:
                    payload += '{"event":' + row + '}'
                    prevsize += len(row) + 10  # 10 bytes is for padding

            if payload:
                print(f"last payload with size {prevsize}")
                postDataToSplunk(props, payload)

        batchDF.toJSON().foreachPartition(f)

    return wrapper
