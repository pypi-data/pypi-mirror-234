import time
import getpass
import platform
import sys
import os
from datetime import datetime

from datahub.emitter import mce_builder as builder
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.metadata.schema_classes import DataFlowInfoClass, DataJobInfoClass, DataJobInputOutputClass,ChangeTypeClass,DatasetPropertiesClass
from datahub.specific.dataset import DatasetPatchBuilder
from datahub.emitter.mce_builder import make_dataset_urn,make_data_job_urn,make_data_flow_urn

import logging
debug = True

if debug:
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.WARNING)
else:
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)

def log(message, v):
    logging.warn(message)
    logging.warn(v)

def get_job_id():
    import __main__
    try:
        filename = __main__.__file__
        filename = os.path.basename(filename)
        if filename.endswith('.py'):
            return filename.split('.')[0]
        return __main__.__file__
    except:
        # return getpass.getuser() + "_" + "notebook"
        return None
    
def get_job_location():
    main_module = sys.modules['__main__']
    try:
        return os.path.abspath(main_module.__file__)
    except:
        return os.getcwd()+'/notebook'
    
# def extract_project_name(path):
#     not_project = ['script', 'dags', 'scripts']
#     if os.path.basename(os.path.dirname(path)) in not_project:
#         return extract_project_name(os.path.dirname(path))
#     else:
#         return os.path.basename(os.path.dirname(path))

def extract_project_name(path):
    return os.path.dirname(path)

def get_flow_id():
    return extract_project_name(get_job_location())
    
def getPipelineName():
    import spark_sdk as ss
    spark = ss.PySpark().spark
    return spark.sparkContext.appName+'-'+spark.sparkContext.applicationId

def getPipelineMaster():
    import spark_sdk as ss
    spark = ss.PySpark().spark
    return spark.sparkContext.master


    
def get_emitter():
    from datahub.emitter.rest_emitter import DataHubRestEmitter
    from spark_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN
    log("GMS_URL_KEY", GMS_URL_KEY)
    USE_REST_EMITTER = True
    if USE_REST_EMITTER:
        return DataHubRestEmitter(gms_server=GMS_URL_KEY, token = GMS_AUTH_TOKEN)

def make_hdfs_path(hdfs_path):
    from spark_sdk.conf import HADOOP_CONF, HADOOP_PORT
    HADOOP_PREFIX = HADOOP_CONF+":"+str(HADOOP_PORT)
    if "file:" in hdfs_path:
        return hdfs_path
    else:
        if HADOOP_PREFIX not in hdfs_path:
            if "hdfs:///" in hdfs_path:
                hdfs_path = hdfs_path.replace("hdfs:///", HADOOP_PREFIX)
            elif "hdfs:/" in hdfs_path:
                hdfs_path = hdfs_path.replace("hdfs:/", HADOOP_PREFIX)
            else:
                hdfs_path = HADOOP_PREFIX + hdfs_path
        return hdfs_path
    
def emitPythonJob(full_table_name:str=None, hdfs_path:str=None, outputNode=True, flow_id=get_flow_id(), job_id = get_job_id()):
    """
    emitPythonJob(full_table_name = extractFromCatalogTable(catalogTable), outputNode=True)
    """
    if isinstance(full_table_name, str):
        full_table_name = full_table_name.lower()
    
    if job_id:
        try:
            DATASET_ENTITY_TYPE = "dataset"
            DATA_JOB_ENTITY_TYPE = "dataJob"
            DATA_FLOW_ENTITY_TYPE = "dataFlow"
            DATA_FLOW_INFO_ASPECT_NAME = "dataFlowInfo"
            DATA_JOB_INFO_ASPECT_NAME = "dataJobInfo"

            inputDS = []
            outputDS = []

            if not outputNode:
                if full_table_name:
                    inputDS.append(builder.make_dataset_urn("hive", full_table_name))
                if hdfs_path:
                    if "file:" in hdfs_path:
                        inputDS.append(builder.make_dataset_urn("file", make_hdfs_path(hdfs_path)))
                    else:
                        inputDS.append(builder.make_dataset_urn("hdfs", make_hdfs_path(hdfs_path)))
            else:
                if full_table_name:
                    outputDS.append(builder.make_dataset_urn("hive", full_table_name))
                if hdfs_path:
                    if "file:" in hdfs_path:
                        outputDS.append(builder.make_dataset_urn("file", make_hdfs_path(hdfs_path)))
                    else:
                        outputDS.append(builder.make_dataset_urn("hdfs", make_hdfs_path(hdfs_path)))



            # Create an emitter to DataHub over REST
            emitter = get_emitter()

            # Add dataflow
            metadata_event = MetadataChangeProposalWrapper(
                entityUrn=builder.make_data_flow_urn(orchestrator='python', flow_id=flow_id),
                aspect=DataFlowInfoClass(
                    name = flow_id,
                    customProperties = {"user": getpass.getuser(),
                                       "appId": flow_id,
                                       "appName": flow_id
                                       }
                ),
            )

            emitter.emit(metadata_event)

            ############# ADD LINEAGE DATAJOB #############
            mcpJobIO = MetadataChangeProposalWrapper(
                entityUrn=builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id),
                aspect=DataJobInputOutputClass(
                    inputDatasets = inputDS,
                    outputDatasets = outputDS
                )
            )
            emitter.emit(mcpJobIO)


            ############# Add info DATAJOB ###############
            property_map_to_set = {"user": getpass.getuser(),
                                "appId": job_id,
                                "appName": job_id,
                                "completedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                                "location": get_job_location(),
                                "server": platform.node() 
                                }

            data_job_info = DataJobInfoClass(
                name=job_id,
                type="SnapshotETL",
                customProperties = property_map_to_set,
                flowUrn=builder.make_data_flow_urn(orchestrator='python', flow_id=flow_id),
            )

            mcpJobInfo = MetadataChangeProposalWrapper(
                    entityType=DATA_JOB_ENTITY_TYPE,
                    changeType=ChangeTypeClass.UPSERT,
                    entityUrn=builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id),
                    aspectName=DATA_JOB_INFO_ASPECT_NAME,
                    aspect=data_job_info,
                )

            emitter.emit(mcpJobInfo)
        except:
            pass
        


class DatasetLineage:
    def __init__(self):
        self.source = []
        self.sink = []
    def addSink(self, sink=None, _type = 'hive'):
        if sink:
            self.sink.append(builder.make_dataset_urn(_type, sink))
    def addSinkUrn(self, sink=None, _type = 'hive'):
        if sink:
            self.sink.append(sink)
    def addSource(self, source, _type = 'hive'):
        self.source.append(builder.make_dataset_urn(_type, source))
    def addSourceUrn(self, source, _type = 'hive'):
        self.source.append(source)
    
    
class DataJobLineage:
    def __init__(self):
        self.source = []
        self.sink = []
    def addSink(self, flow_id, sink=None, _type = 'spark'):
        if sink:
            self.sink = [builder.make_data_job_urn(orchestrator=_type, flow_id=flow_id, job_id = sink)]
    def addSinkUrn(self, sink=None, _type = 'spark'):
        if sink:
            self.sink.append(sink)
    def addSource(self, flow_id, source, _type = 'spark'):
        self.source.append(builder.make_data_job_urn(_type, flow_id=flow_id, job_id = source))
    def addSourceUrn(self, source, _type = 'spark'):
        self.source.append(source)

        
def McpFlowInfo(flow_id):
    ############# ADD DATAFLOW #############
    mcpFlowInfo = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_flow_urn(orchestrator='python', flow_id=flow_id),
        aspect=DataFlowInfoClass(
            name = flow_id,
            customProperties = {"user": getpass.getuser(),
                               "appId": flow_id,
                               "appName": flow_id
                               }
        ),
    )
    return mcpFlowInfo

def McpJobInfo(flow_id, job_id, lineage, _type = 'python'):
    DATASET_ENTITY_TYPE = "dataset"
    DATA_JOB_ENTITY_TYPE = "dataJob"
    DATA_FLOW_ENTITY_TYPE = "dataFlow"
    DATA_FLOW_INFO_ASPECT_NAME = "dataFlowInfo"
    DATA_JOB_INFO_ASPECT_NAME = "dataJobInfo"
    
    ############# ADD LINEAGE DATAJOB #############
    log("DEBUG python job", builder.make_data_job_urn(orchestrator=_type, flow_id=flow_id, job_id = job_id))
    mcpJobIO = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_job_urn(orchestrator=_type, flow_id=flow_id, job_id = job_id),
        aspect=DataJobInputOutputClass(
            inputDatasets = lineage.source,
            outputDatasets = lineage.sink
        )
    )

    ############# Add info DATAJOB ###############
    customProperties = {"user": getpass.getuser(),
                        "appId": job_id,
                        "appName": job_id,
                        "completedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                        "location": get_job_location(),
                        "server": platform.node() 
                        }

    data_job_info = DataJobInfoClass(
        name=job_id,
        type="SnapshotETL",
        customProperties = customProperties,
        flowUrn=builder.make_data_flow_urn(orchestrator='python', flow_id=flow_id),
    )

    mcpJobInfo = MetadataChangeProposalWrapper(
            entityType=DATA_JOB_ENTITY_TYPE,
            changeType=ChangeTypeClass.UPSERT,
            entityUrn=builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id),
            aspectName=DATA_JOB_INFO_ASPECT_NAME,
            aspect=data_job_info,
        )
    
    return (mcpJobIO,mcpJobInfo)


def McpDataset(urn, _type='file'):
    # urn = builder.make_dataset_urn(_type, x)
    dataset_properties = DatasetPropertiesClass(
        customProperties={
             "governance": "ENABLED"
        })

    mcpDataset = MetadataChangeProposalWrapper(
        entityUrn=urn,
        aspect=dataset_properties,
    )
    return mcpDataset

def query_table_schema(urn):
    import requests
    from spark_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN
    url = GMS_URL_KEY+'/api/graphql/'
    query = """
    query {
      dataset(urn: "%s") {
        urn
        container {
          lastIngested
        }
      }
    }
    """ % urn
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:duyvnc'}
    try:
        r = requests.post(url, headers=headers, json=json)
        return r.json()
    except:
        pass
    return None

def check_exist_dataset(urn):
    r = query_table_schema(urn)
    if r:
        if r['data']['dataset']['container']:
            return True
    return False

def SQLQueryExecStartEvent(flow_id, app_id, lineage):    
    ############# ADD DATAFLOW #############
    mcpFlowInfo = McpFlowInfo(flow_id)
    
    ############# ADD DATAFLOW #############
    mcpJobIO, mcpJobInfo = McpJobInfo(flow_id, app_id, lineage)
    
    mcpDataset = []
    for urn in lineage.source:
        if not check_exist_dataset(urn):
            mcpDataset.append(McpDataset(urn))
    
    for urn in lineage.sink:
        if not check_exist_dataset(urn):
            mcpDataset.append(McpDataset(urn))
    mcpDataset.extend((mcpFlowInfo,mcpJobIO,mcpJobInfo))
    return mcpDataset


def emit(mcpws):
    emitter = get_emitter()
    for mcp in mcpws:
        if mcp:
            try:
                emitter.emit(mcp)
            except Exception as e:
                log("Error to emit", mcp)
                log("Error to emit", e)
            
            
def drilldown(logicalPlan):
    all_relation = []
    if 'catalogTable' in dir(logicalPlan):
        if logicalPlan.catalogTable().__str__() != 'None':
            all_relation.append(logicalPlan.catalogTable().get().qualifiedName())
        elif 'relation' in dir(logicalPlan):
            all_relation.append(logicalPlan.relation().location().rootPaths().head().toString())

    if 'children' in dir(logicalPlan):
        children = logicalPlan.children()
        if 'display0' in dir(children):
            for Jobject in children.display0():
                if 'catalogTable' in dir(Jobject):
                    if Jobject.catalogTable().__str__() != 'None':
                        all_relation.append(Jobject.catalogTable().get().qualifiedName())
                    elif 'relation' in dir(Jobject):
                        all_relation.append(Jobject.relation().location().rootPaths().head().toString())
                elif Jobject:
                    all_relation.extend(drilldown(Jobject))
    
    return all_relation


def extractcatalogTableFromlogicalPlan(logicalPlan):
    all_relation = []
    if 'child' in dir(logicalPlan):
        child = logicalPlan.child()
        all_relation.extend(drilldown(child))
    else:
        all_relation.extend(drilldown(logicalPlan))
        
        
    if 'children' in dir(logicalPlan):
        children = logicalPlan.children()
        if 'array' in dir(children):
            for child in list(a.children().array()):
                if child:
                    all_relation.extend(drilldown(child))
    return all_relation


def extractFromCatalogTable(catalogTable):
    return catalogTable.qualifiedName()


def getLastestJobId(flow_id, master):
    import requests
    from spark_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN
    url = GMS_URL_KEY+'/api/graphql/'
    cookies={''}
    query = """query getDataFlow($urn: String!) {
      dataFlow(urn: $urn) {
        childJobs: relationships(
          input: {types: ["IsPartOf"], direction: INCOMING, start: 0, count: 100}
        ) {
          start
          count
          total
          relationships {
            entity {
              ... on DataJob {
                urn
                type
                jobId
                properties {
                  name
                  description
                  customProperties {
                    key
                    value
                  }
                  __typename
                }
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
    }

    """
    json = {"operationName":"getDataFlow","variables":{"urn":f"urn:li:dataFlow:(spark,{flow_id},{master})"},"query":query}
    log("getLastestJobId json", json)
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub', 'Authorization': f'Bearer {GMS_AUTH_TOKEN}'}
    
    lastest = []
    try:
        r = requests.post(url, headers=headers, json=json)
        dataFlow = r.json()
        log("dataFlow", dataFlow)

    except Exception as e: 
        log("getLastestJobId",e)
        return False
    return lastestdataJob(dataFlow)

def getLineage(urn, direction="UPSTREAM"):
    import requests
    from spark_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN
    url = GMS_URL_KEY+'/api/graphql/'
    query = """
query {
  dataset(
      urn: """+f'"{urn}"'+""") {
    lineage (input: {
        direction: """+direction+"""}) {
        total
        relationships {
            type
            degree
            createdOn
            createdActor {
              urn
              type
            }
            entity {
                urn
                type
                relationships(input:{
                    direction: OUTGOING 
                    types:"DATASET"
              }) {
                start
                count
                total
              }
            }
        }
    }
  }
}
    """
    cookies={''}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub', 'Authorization': f'Bearer {GMS_AUTH_TOKEN}'}
    json={'query': query}
    try:
        r = requests.post(url, headers=headers, json=json)
        return r.json()
    except:
        pass
    return None
    
def lastestdataJob(dataFlow):
    lastest = dict()
    lastest['completedAt'] = '0000'
    
    if dataFlow['data']['dataFlow']['childJobs']['relationships']:
        log("dataFlow['data']['dataFlow']['childJobs']['relationships']", dataFlow['data']['dataFlow']['childJobs']['relationships'])
        for datajob in dataFlow['data']['dataFlow']['childJobs']['relationships']:
            if datajob['entity']['properties']['customProperties']:
                log("datajob['entity']['properties']['customProperties']", datajob['entity']['properties']['customProperties'])
                for k in datajob['entity']['properties']['customProperties']:
                    if k['key'] == 'completedAt':
                        log("k['value']", k['value'])
                        if k['value'] > lastest['completedAt']:
                            lastest['urn'] =  datajob['entity']['urn']
                            lastest['completedAt'] = k['value']
                            log("lastest['urn']", lastest['urn'])
    if 'urn' in lastest:
        return lastest['urn']
    return False
    
    
def addLineage(upstreamUrn, downstreamUrn):
    import requests
    from spark_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN
    url = GMS_URL_KEY+'/api/graphql/'
    query = """
    mutation {
  updateLineage (input:{
    edgesToAdd: [{
      upstreamUrn: """+f'"{upstreamUrn}"'+""",
      downstreamUrn: """+f'"{downstreamUrn}"'+"""
    }]
    })
    }
    """
    cookies={''}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub', 'Authorization': f'Bearer {GMS_AUTH_TOKEN}'}
    json={'query': query}
    try:
        r = requests.post(url, headers=headers, json=json)
    except Exception as e: 
        log("addLineage",e)
    return r.json()


# def addLineageAfterToDwh():
#     WAIT_TIME = 20
#     lineage = DatasetLineage()
#     wait_time = 0
#     poke_every = 5
#     while len(lineage.sink)==0 and wait_time < WAIT_TIME:
#         sparkUrn = getLastestJobId(getPipelineName(), getPipelineMaster())
    
#         if sparkUrn:
#             flow_id=get_flow_id()
#             job_id = get_job_id()
#             pythonUrn = builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id)
#             # lineage = DataJobLineage()
#             # lineage.addSinkUrn(sparkUrn)

#             dataset = getLineage(sparkUrn)
#             if dataset:
#                 if dataset['data']['dataset']['lineage']['relationships']:
#                     for x in dataset['data']['dataset']['lineage']['relationships']:
#                         lineage.addSinkUrn(x['entity']['urn'])
#         import time
#         time.sleep(poke_every)
#         wait_time += poke_every
        

#     if lineage.sink:
#         mcpws = mcpJobInfo(flow_id, job_id, lineage)
#         emit(mcpws)
        
#     logging.warning("sparkUrn")
#     logging.warning(sparkUrn)
#     logging.warning("pythonUrn")
#     logging.warning(pythonUrn)
#     logging.warning("lineage")
#     logging.warning(lineage.sink)


def scanVariable(variable_name, txt):
    import re
    pattern_var1 = r'{x}\s*=\s*["\']([^"\']+)["\']'.format(x = variable_name)
    matches_api1 = re.findall(pattern_var1, txt)
    if matches_api1:
        return matches_api1
    
    pattern_api2 = r'{x}\s*=\s*["\'\f]([^"\']+)["\']'.format(x = variable_name)
    matches_api2 = re.findall(pattern_var1, txt)
    if matches_api2:
        return matches_api2
    
    pattern_assign = r'{x}\s*=\s*(\w+)'.format(x = variable_name)
    matches_assign = re.findall(pattern_assign, txt)
    for variable_name in matches_assign:
        return scanVariable(variable_name, txt)
    return None


def parseUrl2Urn(url):
    from urllib.parse import urlparse
    return urlparse(url).netloc + urlparse(url).path.rstrip("/")


def add_abspath(path):
    if '/' not in path:
        return os.path.join(os.getcwd(), path)
    return path

def scanPattern(pattern_prefix, txt, _type, lineage, direction='source'):
    import re
    pattern_simple = r'{x}["\']([^"\']+)["\']'.format(x=pattern_prefix)
    matches_simple = re.findall(pattern_simple, txt)
    if _type == 'api':
        matches_simple = [parseUrl2Urn(x) for x in matches_simple]
    _ = [lineage.addSource(f, _type = _type) for f in matches_simple if f]
    log("matches_simple", matches_simple)

    pattern_fstring = r'{x}f["\']([^"\']+)["\']'.format(x=pattern_prefix)
    matches_fstring = re.findall(pattern_fstring, txt)
    log("matches_fstring", matches_fstring)
    for full_fstring in matches_fstring:
        variables = re.findall(r'\{(.+?)\}', full_fstring)
        for variable_name in variables:
            matches_var = scanVariable(variable_name, txt)
            log("matches_var", matches_var)
            if matches_var:
                full_fstring = full_fstring.replace("{" + variable_name + "}", matches_var[0])
            
        if _type == 'api':
            full_fstring = parseUrl2Urn(full_fstring)
        if full_fstring:
            if direction == 'source':
                lineage.addSource(add_abspath(full_fstring), _type = _type)
                log("full_fstring source", full_fstring)
            else:
                lineage.addSink(add_abspath(full_fstring), _type = _type)
                log("full_fstring sink", full_fstring)
    return lineage
    

def scanPythonFile(lineage):
    import re
    try:
        txt = open(get_job_location(), 'r').read()
        # txt = open(get_job_location(), 'r').read()
        x = ''
        for line in txt.split("\n"):
            if not line.strip().startswith("#"):
                x += line + '\n'
        txt = x
    except:
        txt = ''
    
    if 'requests.post(' in txt or 'request("post"' in txt or 'requests.get(' in txt or 'request("get"' in txt:
        lineage = scanPattern(pattern_prefix = "url\s*=\s*", txt = txt, _type = 'api', lineage = lineage, direction='source')
    lineage = scanPattern(pattern_prefix = "pd\.read_csv\(", txt = txt, _type = 'file', lineage = lineage, direction='source')
    lineage = scanPattern(pattern_prefix = "pd\.read_excel\(", txt = txt, _type = 'file', lineage = lineage, direction='source')
    lineage = scanPattern(pattern_prefix = ".to_csv\(", txt = txt, _type = 'file', lineage = lineage, direction='sink')
    return lineage




def addLineageAfterToDwh(full_table_name):
    full_table_name = full_table_name.lower()
    lineage = DatasetLineage()
    lineage.addSink(full_table_name)
    
    lineage = scanPythonFile(lineage)
    
    flow_id=get_flow_id()
    job_id = get_job_id()
    
    log("lineage.sink", lineage.sink)
    log("len(lineage.source)", len(lineage.source))
    log("ineage.source", lineage.source)
    log("job_id", job_id)
    log("flow_id", flow_id)
    if job_id: # and len(lineage.source)>0:
        pythonUrn = builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id)
        dataset = getLineage(pythonUrn, "UPSTREAM")
        for x in dataset['data']['dataset']['lineage']['relationships']:
            lineage.addSourceUrn(x['entity']['urn'])
            log("x['entity']['urn']", x['entity']['urn'])

        dataset = getLineage(pythonUrn, "DOWNSTREAM")
        for x in dataset['data']['dataset']['lineage']['relationships']:
            lineage.addSinkUrn(x['entity']['urn'])
            log("x['entity']['urn']", x['entity']['urn'])

        mcpws = SQLQueryExecStartEvent(flow_id, job_id, lineage)
        log("mcpws addLineageAfterToDwh", mcpws)
        emit(mcpws)
            
        log("addLineageAfterToDwh pythonUrn", pythonUrn)
        log("addLineageAfterToDwh lineage sink", lineage.sink)
        log("addLineageAfterToDwh lineage source", lineage.source)
    return True



####################################################
import sys
from collections import Counter
from typing import List, Optional, Type, Union, no_type_check, overload, TYPE_CHECKING
from warnings import catch_warnings, simplefilter, warn

from pyspark.rdd import _load_from_socket
from pyspark.sql.pandas.serializers import ArrowCollectSerializer
from pyspark.sql.types import (
    IntegralType,
    ByteType,
    ShortType,
    IntegerType,
    LongType,
    FloatType,
    DoubleType,
    BooleanType,
    MapType,
    TimestampType,
    TimestampNTZType,
    DayTimeIntervalType,
    StructType,
    DataType,
)
from pyspark.sql.utils import is_timestamp_ntz_preferred
from pyspark.traceback_utils import SCCallSiteSync

if TYPE_CHECKING:
    import numpy as np
    import pyarrow as pa
    from py4j.java_gateway import JavaObject

    from pyspark.sql.pandas._typing import DataFrameLike as PandasDataFrameLike
    from pyspark.sql import DataFrame

    
    
class PandasConversionMixin:
    """
    Mix-in for the conversion from Spark to pandas. Currently, only :class:`DataFrame`
    can use this class.
    """

    def toPandasLineage(self) -> "PandasDataFrameLike":
        """
        Returns the contents of this :class:`DataFrame` as Pandas ``pandas.DataFrame``.

        This is only available if Pandas is installed and available.

        .. versionadded:: 1.3.0

        Notes
        -----
        This method should only be used if the resulting Pandas ``pandas.DataFrame`` is
        expected to be small, as all the data is loaded into the driver's memory.

        Usage with ``spark.sql.execution.arrow.pyspark.enabled=True`` is experimental.

        Examples
        --------
        >>> df.toPandas()  # doctest: +SKIP
           age   name
        0    2  Alice
        1    5    Bob
        """

        log("USING toPandasLineage", "Start")
        # ========================LINEAGE======================
        try:
            logicalPlan = self._jdf.logicalPlan()
            flow_id=get_flow_id()
            job_id = get_job_id()
            if job_id:
                lineage = DatasetLineage()
                for catalogTable in extractcatalogTableFromlogicalPlan(logicalPlan):
                    lineage.addSource(catalogTable)

                pythonUrn = builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id)
                dataset = getLineage(pythonUrn, "UPSTREAM")
                for x in dataset['data']['dataset']['lineage']['relationships']:
                    log("Append UPSTREAM toPandas", x['entity']['urn'])
                    lineage.addSourceUrn(x['entity']['urn'])
                    log("x['entity']['urn']", x['entity']['urn'])

                dataset = getLineage(pythonUrn, "DOWNSTREAM")
                for x in dataset['data']['dataset']['lineage']['relationships']:
                    log("Append DOWNSTREAM toPandas", x['entity']['urn'])
                    lineage.addSinkUrn(x['entity']['urn'])
                    log("x['entity']['urn']", x['entity']['urn'])

                mcpws = SQLQueryExecStartEvent(flow_id, job_id, lineage)
                log("mcpws toPandas", mcpws)
                emit(mcpws)
        except:
            pass
        # =====================================================

        from pyspark.sql.dataframe import DataFrame

        assert isinstance(self, DataFrame)

        from pyspark.sql.pandas.utils import require_minimum_pandas_version

        require_minimum_pandas_version()

        import numpy as np
        import pandas as pd
        from pandas.core.dtypes.common import is_timedelta64_dtype

        jconf = self.sparkSession._jconf
        timezone = jconf.sessionLocalTimeZone()

        if jconf.arrowPySparkEnabled():
            use_arrow = True
            try:
                from pyspark.sql.pandas.types import to_arrow_schema
                from pyspark.sql.pandas.utils import require_minimum_pyarrow_version

                require_minimum_pyarrow_version()
                to_arrow_schema(self.schema)
            except Exception as e:

                if jconf.arrowPySparkFallbackEnabled():
                    msg = (
                        "toPandas attempted Arrow optimization because "
                        "'spark.sql.execution.arrow.pyspark.enabled' is set to true; however, "
                        "failed by the reason below:\n  %s\n"
                        "Attempting non-optimization as "
                        "'spark.sql.execution.arrow.pyspark.fallback.enabled' is set to "
                        "true." % str(e)
                    )
                    warn(msg)
                    use_arrow = False
                else:
                    msg = (
                        "toPandas attempted Arrow optimization because "
                        "'spark.sql.execution.arrow.pyspark.enabled' is set to true, but has "
                        "reached the error below and will not continue because automatic fallback "
                        "with 'spark.sql.execution.arrow.pyspark.fallback.enabled' has been set to "
                        "false.\n  %s" % str(e)
                    )
                    warn(msg)
                    raise

            # Try to use Arrow optimization when the schema is supported and the required version
            # of PyArrow is found, if 'spark.sql.execution.arrow.pyspark.enabled' is enabled.
            if use_arrow:
                try:
                    from pyspark.sql.pandas.types import (
                        _check_series_localize_timestamps,
                        _convert_map_items_to_dict,
                    )
                    import pyarrow

                    # Rename columns to avoid duplicated column names.
                    tmp_column_names = ["col_{}".format(i) for i in range(len(self.columns))]
                    self_destruct = jconf.arrowPySparkSelfDestructEnabled()
                    batches = self.toDF(*tmp_column_names)._collect_as_arrow(
                        split_batches=self_destruct
                    )
                    if len(batches) > 0:
                        table = pyarrow.Table.from_batches(batches)
                        # Ensure only the table has a reference to the batches, so that
                        # self_destruct (if enabled) is effective
                        del batches
                        # Pandas DataFrame created from PyArrow uses datetime64[ns] for date type
                        # values, but we should use datetime.date to match the behavior with when
                        # Arrow optimization is disabled.
                        pandas_options = {"date_as_object": True}
                        if self_destruct:
                            # Configure PyArrow to use as little memory as possible:
                            # self_destruct - free columns as they are converted
                            # split_blocks - create a separate Pandas block for each column
                            # use_threads - convert one column at a time
                            pandas_options.update(
                                {
                                    "self_destruct": True,
                                    "split_blocks": True,
                                    "use_threads": False,
                                }
                            )
                        pdf = table.to_pandas(**pandas_options)
                        # Rename back to the original column names.
                        pdf.columns = self.columns
                        for field in self.schema:
                            if isinstance(field.dataType, TimestampType):
                                pdf[field.name] = _check_series_localize_timestamps(
                                    pdf[field.name], timezone
                                )
                            elif isinstance(field.dataType, MapType):
                                pdf[field.name] = _convert_map_items_to_dict(pdf[field.name])
                        return pdf
                    else:
                        corrected_panda_types = {}
                        for index, field in enumerate(self.schema):
                            pandas_type = PandasConversionMixin._to_corrected_pandas_type(
                                field.dataType
                            )
                            corrected_panda_types[tmp_column_names[index]] = (
                                np.object0 if pandas_type is None else pandas_type
                            )

                        pdf = pd.DataFrame(columns=tmp_column_names).astype(
                            dtype=corrected_panda_types
                        )
                        pdf.columns = self.columns
                        return pdf
                except Exception as e:
                    # We might have to allow fallback here as well but multiple Spark jobs can
                    # be executed. So, simply fail in this case for now.
                    msg = (
                        "toPandas attempted Arrow optimization because "
                        "'spark.sql.execution.arrow.pyspark.enabled' is set to true, but has "
                        "reached the error below and can not continue. Note that "
                        "'spark.sql.execution.arrow.pyspark.fallback.enabled' does not have an "
                        "effect on failures in the middle of "
                        "computation.\n  %s" % str(e)
                    )
                    warn(msg)
                    raise

        # Below is toPandas without Arrow optimization.
        pdf = pd.DataFrame.from_records(self.collect(), columns=self.columns)
        column_counter = Counter(self.columns)

        corrected_dtypes: List[Optional[Type]] = [None] * len(self.schema)
        for index, field in enumerate(self.schema):
            # We use `iloc` to access columns with duplicate column names.
            if column_counter[field.name] > 1:
                pandas_col = pdf.iloc[:, index]
            else:
                pandas_col = pdf[field.name]

            pandas_type = PandasConversionMixin._to_corrected_pandas_type(field.dataType)
            # SPARK-21766: if an integer field is nullable and has null values, it can be
            # inferred by pandas as a float column. If we convert the column with NaN back
            # to integer type e.g., np.int16, we will hit an exception. So we use the
            # pandas-inferred float type, rather than the corrected type from the schema
            # in this case.
            if pandas_type is not None and not (
                isinstance(field.dataType, IntegralType)
                and field.nullable
                and pandas_col.isnull().any()
            ):
                corrected_dtypes[index] = pandas_type
            # Ensure we fall back to nullable numpy types.
            if isinstance(field.dataType, IntegralType) and pandas_col.isnull().any():
                corrected_dtypes[index] = np.float64
            if isinstance(field.dataType, BooleanType) and pandas_col.isnull().any():
                corrected_dtypes[index] = np.object  # type: ignore[attr-defined]

        df = pd.DataFrame()
        for index, t in enumerate(corrected_dtypes):
            column_name = self.schema[index].name

            # We use `iloc` to access columns with duplicate column names.
            if column_counter[column_name] > 1:
                series = pdf.iloc[:, index]
            else:
                series = pdf[column_name]

            # No need to cast for non-empty series for timedelta. The type is already correct.
            should_check_timedelta = is_timedelta64_dtype(t) and len(pdf) == 0

            if (t is not None and not is_timedelta64_dtype(t)) or should_check_timedelta:
                series = series.astype(t, copy=False)

            with catch_warnings():
                from pandas.errors import PerformanceWarning

                simplefilter(action="ignore", category=PerformanceWarning)
                # `insert` API makes copy of data,
                # we only do it for Series of duplicate column names.
                # `pdf.iloc[:, index] = pdf.iloc[:, index]...` doesn't always work
                # because `iloc` could return a view or a copy depending by context.
                if column_counter[column_name] > 1:
                    df.insert(index, column_name, series, allow_duplicates=True)
                else:
                    df[column_name] = series






        if timezone is None:
            return df
        else:
            from pyspark.sql.pandas.types import _check_series_convert_timestamps_local_tz

            for field in self.schema:
                # TODO: handle nested timestamps, such as ArrayType(TimestampType())?
                if isinstance(field.dataType, TimestampType):
                    df[field.name] = _check_series_convert_timestamps_local_tz(
                        df[field.name], timezone
                    )
            return df
        
        
    @staticmethod
    def _to_corrected_pandas_type(dt: DataType) -> Optional[Type]:
        """
        When converting Spark SQL records to Pandas `pandas.DataFrame`, the inferred data type
        may be wrong. This method gets the corrected data type for Pandas if that type may be
        inferred incorrectly.
        """
        import numpy as np

        if type(dt) == ByteType:
            return np.int8
        elif type(dt) == ShortType:
            return np.int16
        elif type(dt) == IntegerType:
            return np.int32
        elif type(dt) == LongType:
            return np.int64
        elif type(dt) == FloatType:
            return np.float32
        elif type(dt) == DoubleType:
            return np.float64
        elif type(dt) == BooleanType:
            return np.bool  # type: ignore[attr-defined]
        elif type(dt) == TimestampType:
            return np.datetime64
        elif type(dt) == TimestampNTZType:
            return np.datetime64
        elif type(dt) == DayTimeIntervalType:
            return np.timedelta64
        else:
            return None
