import os
from spark_sdk import conf

import findspark
findspark.init(os.getenv("SPARK_HOME"))

import sys
from .utils import choose_num_core, choose_executor_memory, choose_driver_memory, _check_series_convert_timestamps_internal, _get_local_timezone, contains_duplicates, modulereload
from .hive_metastore import HiveMetastoreClient

import json

import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from pyarrow import fs


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class Utf8Encoder(object):
    def __init__(self, fp):
        self.fp = fp

    def write(self, data):
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        self.fp.write(data)

        
# display options
try:
    import IPython
    IPython.auto_scroll_threshold = 100000

    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "all"
    from IPython.display import display

    from IPython.core.display import HTML
    display(HTML("<style>pre { white-space: pre !important; }</style>"))

except Exception as e:
    print(e)

pd.options.display.max_columns = 50


from typing import (Union)

class PySpark:
    def __init__(self, driver_memory='1G', num_executors='1', executor_memory='4G', port='', yarn=False, **spark_configs):
        """
         Parameters
        ----------

        driver_memory: memory for spark driver and executor memory, must less than 8Gb. 8Gb is handle table 10 milion rows
        executor_memory: memeory for core spark, must less than 8G
        core: executor core, must less than 10 cores
        port: change port if user false job
        yarn: (boolan) if True is run with yarn mode, if False run with local mode
        spark_configs: add more extensions by add_on1 = ("spark.dynamicAllocation.enabled", "true")
        """

        self.driver_memory = driver_memory
        self.executor_memory = executor_memory
        self.num_executors = num_executors
        self.port = port

        if yarn:
            self.yarn = 'yarn'
        else:
            self.yarn = f'local[{self.num_executors}]'

        # create spark session
        import pyspark
        from pyspark import SparkConf
        from pyspark.sql import SparkSession
        from pyspark.sql import SQLContext

        conf = SparkConf()

        # config spark application name
        import getpass
        conf.setAppName(f"spark_sdk_{getpass.getuser()}")

        # config location for spark finding metadata from hive metadata server
        from spark_sdk.conf import (HIVE_IP_NODES1, HIVE_IP_NODES2)
        conf.set("hive.metastore.uris", HIVE_IP_NODES1+","+HIVE_IP_NODES2)
        conf.set("spark.sql.hive.metastore.jars", "/opt/spark/spark-3.0.2-bin-hadoop2.7/*")


        # config in-memory columnar data format that is used in Spark to efficiently transfer data between JVM and Python processes
        conf.set("spark.kryoserializer.buffer.max", "2000")
        conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
        # conf.set("spark.sql.execution.arrow.enabled", "true") # remove in future
        conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "10000")
        
        if self.yarn == 'yarn':
            #queue
            conf.set("spark.yarn.queue", "batch")
            
            # config spark dynamicAllocation
            conf.set("spark.dynamicAllocation.enabled", "true")
            conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
            conf.set("spark.dynamicAllocation.minExecutors", 1)
            conf.set("spark.dynamicAllocation.maxExecutors", 8)
            conf.set("spark.dynamicAllocation.executorIdleTimeout", "300s")
            conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
            conf.set("spark.dynamicAllocation.shuffleTracking.timeout", "300s")
        else:
            # config directory to use for "scratch" space in Spark, including map output files and RDDs that get stored on disk
            conf.set('spark.local.dir', '/tmp')
            
            conf.set("spark.dynamicAllocation.enabled", "true")
            conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
            conf.set("spark.dynamicAllocation.minExecutors", 1)
            conf.set("spark.dynamicAllocation.maxExecutors", 10)
            conf.set("spark.dynamicAllocation.executorIdleTimeout", "300s")
            conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
            conf.set("spark.dynamicAllocation.shuffleTracking.timeout", "300s")


        # config partition Size
        # conf.set('spark.sql.adaptive.coalescePartitions.minPartitionSize', '128MB')
        conf.set('spark.sql.files.minPartitionNum', 100000)

        # config spark driver memory
        conf.set("spark.driver.memory", self.driver_memory)
        conf.set('spark.executor.memory', self.executor_memory)
        conf.set('spark.driver.maxResultSize', '10G')

        if int(self.num_executors) > 1:
            conf.set('spark.num.executors', int(self.num_executors))
            conf.set('spark.executor.cores', 4)
        conf.set('spark.rpc.message.maxSize', '1000')

        # conf.set("spark.ui.enabled", "false")
        if not port:
            port = 0
            for j,i in enumerate(getpass.getuser()):
                port+=ord(i) * 1 if j//2 == 1 else -1
            port +=4300
        conf.set("spark.ui.port", port)
        conf.set("spark.port.maxRetries", "30")

        # config for write append parquet
        conf.set("spark.sql.parquet.compression.codec", "snappy")

        # set metastore.client.capability.check to false
        conf.set("hive.metastore.client.capability.check", "false")

        # config for descrypt data
        from spark_sdk.conf import LIST_JARS
        if LIST_JARS:
            conf.set("spark.jars", LIST_JARS)
            
        # conf.set("spark.jars", "hdfs:///shared/jars/hotpot_2.12-0.0.3.jar")
        conf.set("spark.sql.redaction.string.regex", ".{22}==")
        
        # delta format
        conf.set("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog")
        conf.set("spark.sql.extensions","io.delta.sql.DeltaSparkSessionExtension")
        conf.set("spark.sql.catalogImplementation","hive")
        conf.set('spark.sql.hive.metastorePartitionPruningFallbackOnException', True)
        conf.set('spark.sql.hive.metastorePartitionPruningFastFallback', True)
        conf.set("spark.databricks.delta.optimize.maxFileSize", 268435456) # 256MB
        conf.set('spark.databricks.delta.retentionDurationCheck.enabled', False)
        # conf.set('spark.jars.packages', "io.delta:delta-core_2.12:2.1.0")
        # conf.set("spark.driver.extraJavaOptions", "-Dhttps.proxyHost=proxy.hcm.fpt.vn -Dhttps.proxyPort=80 -Dhttp.proxyHost=proxy.hcm.fpt.vn -Dhttp.proxyPort=80")
        # conf.set("spark.executor.extraJavaOptions", "-Dhttps.proxyHost=proxy.hcm.fpt.vn -Dhttps.proxyPort=80 -Dhttp.proxyHost=proxy.hcm.fpt.vn -Dhttp.proxyPort=80")
        
        # fix legacy parquet timestamp error
        conf.set("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED")
        conf.set("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
        conf.set("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED")
        conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")
        
        # lineage
        from spark_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN, LIST_JARS
        if LIST_JARS:
            if "datahub-spark-lineage" in LIST_JARS:
                conf.set("spark.extraListeners","datahub.spark.DatahubSparkListener")
                conf.set("spark.datahub.rest.server", GMS_URL_KEY)
                conf.set("spark.datahub.rest.token", GMS_AUTH_TOKEN)
        

        all_config = {c[0]:c[1] for c in conf.getAll()}
        for k_c in spark_configs.keys():
            if len(spark_configs[k_c]) == 2:
                if spark_configs[k_c][0] in ['spark.repl.local.jars', 'spark.sql.hive.metastore.jars', 'spark.jars']:
                    conf.set(spark_configs[k_c][0], all_config[spark_configs[k_c][0]]+','+spark_configs[k_c][1])
                else:
                    conf.set(spark_configs[k_c][0], spark_configs[k_c][1])
            else:
                raise TypeError(f"PySpark got an unexpected keyword argument {k_c}")
        
        self.spark = SparkSession.builder.config(conf=conf).master(self.yarn).enableHiveSupport().getOrCreate()
            
        # config timezone
        self.spark.conf.set('spark.sql.session.timeZone', '+07:00')

        # config show pandas dataframe format on notebook
        self.spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
        self.spark.conf.set("spark.sql.repl.eagerEval.truncate", 200)

        self.spark.conf.get("hive.metastore.uris")

        # defing decrypt function
        try:
            self.spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fdecrypt", "fdecrypt")
            self.spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fencrypt", "fencrypt")
            self.spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fmask", "fmask")
        except:
            pass
        
        # dont print WARN
        self.spark.sparkContext.setLogLevel("ERROR")
        
        
    

    def get_fs(self):
        # get hadoop file system
        return self.spark._jvm.org.apache.hadoop.fs.FileSystem.get(self.spark._jsc.hadoopConfiguration())

    def check_is_file(self, hdfs_path):
        fs = self.get_fs()
        return fs.exists(self.spark._jvm.org.apache.hadoop.fs.Path(hdfs_path))

    def _to_java_object_rdd(self, rdd):
        from pyspark.serializers import PickleSerializer, AutoBatchedSerializer
        """ Return a JavaRDD of Object by unpickling
        It will convert each Python object into Java object by Pyrolite, whenever the
        RDD is serialized in batch or not.
        """
        rdd = rdd._reserialize(AutoBatchedSerializer(PickleSerializer()))
        JavaObj = rdd.ctx._jvm.org.apache.spark.mllib.api.python.SerDe.pythonToJava(rdd._jrdd, True)

        return JavaObj

    def convert_size(self, size_bytes):
        '''
        return at MB
        '''
        return size_bytes / 1024 / 1024

    def num_repartition(self, sparkDF):
        '''
        Number Partition
        If file < 128MB ==> num_partition = 1
        If file between 128MB and 256MB ==> num_partition = 2
        '''
        memory_byte = self.spark._jvm.org.apache.spark.util.SizeEstimator.estimate(
            self._to_java_object_rdd(sparkDF.rdd))

        memory_mb = self.convert_size(memory_byte)

        return int(memory_mb // (128 * 300) + 1)

    def check_keys_path_format(self, keys_path):
        import re
        if re.search('json$', keys_path):
            return True
        else:
            raise Exception("keys_path must end with '.json'")

    def autogenerate_key(self, length_key=22):
        """
        Input length of string key
        return random string (contains string upper case and string lower case) and digits 
        """
        import string
        import random

        key = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length_key))
        key = key + "=="
        return key

    def auto_generate_list_keys(self, table_name, column_name='', keys_path='keys.json'):
        """
        Input
        table_name: Name of table that need encrypt
        column_name: list string seperate by ',', ex: a,b,c
        keys_path: path file of key if want to append key to file
        
        return list of keys ready to be copy
        """
        from datetime import datetime
        import json

        if self.check_is_file(keys_path):
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        for c in column_name.split(','):
            if c:
                keys = {}

                keys["name"] = f"secret_for_{table_name}_{c}"
                keys["description"] = f"This is secret_for_{table_name}_{c}"
                keys["created"] = round(datetime.timestamp(datetime.now()))
                keys["material"] = self.autogenerate_key()

                list_keys.append(keys)
        return list_keys
    
    def encrypt_column(self, sparkDF, table_name, column_names=[], keys_path=''):
        """
        Input
        : sparkDF: spark.sql.DataFrame
        : table_name: name of table example: table1
        : column_names: list column name need encrypt
        : keys_path: json path example: /path/to/keys.json
        return: spark.sql.DataFrame have encrypted column
        """
        # check file keys exist
        if self.check_is_file(keys_path):
            # Opening JSON file
            list_keys = PyArrow().read_json(keys_path)
        else:
            list_keys = []

        keys_exist = {}
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            # check if key in file
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]

        for c in column_names:
            # if not found key generate new key append to keys.json
            if c not in keys_exist.keys():
                print('Append key for', c)
                PyArrow().append_keys_to_file(table_name, c, keys_path)

        list_keys = PyArrow().read_json(keys_path)
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]

        fields = "\n                "
        comma = ",\n                "

        for s in sparkDF.schema:
            c = s.name
            if c in column_names:
                field_dev = f"""fencrypt({c}, '{keys_exist[c]}') as {c}{comma}"""
            else:
                field_dev = f"{c}{comma}"

            fields += field_dev

        fields = fields[:-len(comma)]

        sql = f"""
        SELECT 
            {fields}
        FROM {table_name}
        """

        sparkDF.createOrReplaceTempView(f"{table_name}")
        print('Start encrypt column')

        return self.spark.sql(sql)

    def read_first_file(self, database, table_name, hdfs_path):
        '''
        Read schema hive
        '''
        try:
            df = self.spark.sql(f"""SELECT * FROM {database}.{table_name} LIMIT 5""")
        except:
            if 'parquet' in hdfs_path:
                df = self.spark.sql(f"""SELECT * FROM parquet.`{hdfs_path}` LIMIT 5""")
            else:
                raise AnalysisException(f"Table or view not found {database}.{table_name}")
        return df

    def compare_data_type(self, first_sparkDF, second_sparkDF):
        """
        Function to check when write data second time
        """                             
        def get_data_type(datatype):
            mapping = {'LongType()': 'IntegerType()', 'IntegerType()': 'LongType()'}
            if datatype in mapping.keys():
                return mapping[datatype]
            else:
                return datatype
            
        error = {}
        if len(first_sparkDF.schema) == len(second_sparkDF.schema):
            for c in second_sparkDF.schema:
                c_name = c.name
                second_type = second_sparkDF.schema[c_name].dataType
                second_type = str(second_type)
                first_type = first_sparkDF.schema[c_name].dataType
                first_type = str(first_type)

                if first_type != second_type:
                    if first_type != get_data_type(second_type):
                        error[c_name] = {'first_time': first_type, 'second_time': second_type}
                             
                if error.keys():
                    print('Error', error)
                    first_sparkDF.unpersist()
                    second_sparkDF.unpersist()
                    raise TypeError(f"DataType of Columns this time store is not like first time {error}")
        else:
            print(f'First time have columns', first_sparkDF.schema.names)
            print(f'Second time have columns', second_sparkDF.schema.names)
            
            raise ValueError(f"First time have {len(first_sparkDF.schema)} columns but second time have {len(second_sparkDF.schema)} columns")
        
                             

        print('Check schema OK')
        first_sparkDF.unpersist()

    def query_yes_no(self, question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
                It must be "yes" (the default), "no" or None (meaning
                an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

    def create_table_and_metadata(self, database, table_name, hdfs_path, partition_by=''):
        """
        Create table in catalog and MSCK (update metadata) if partitioned table
        Input:
        :param database: database name, example: default
        :param table_name: table name, example: test1
        :param hdfs_path: path to data, example /path/to/data.parquet
        Return:
        nothing
        """
        if database and table_name:
            try:
                self.spark.catalog.createTable(database + '.' + table_name, "hdfs://" + hdfs_path)
            except:
                # AnalysisException table aready exists
                print('Cannot create table, this table already exists ==> repair data')

        elif database and not table_name:
            raise Exception("You must add parameters table_name=")

        elif not database and table_name:
            raise Exception("You must add database=")

        if partition_by:
            print('MSCK REPAIR DATA FOR PARTITION TABLE')
            self.spark.sql(f'msck REPAIR TABLE {database}.{table_name}')
            
        self.spark.sql(f"""REFRESH TABLE {database}.{table_name}""")

    def store_spark_dataframe_to_dwh(self, data, hdfs_path, repartition=False, numPartitions=None, partition_by='',
                                     partition_date='', compression = 'snappy', 
                                     database='', table_name='', encrypt_columns=[], keys_path=''):
        """
         Parameters
        ----------
        data: pyspark.sql.dataframe.DataFrame
        hdfs_path : Path hdfs user want to store. EX: /data/fpt/ftel/cads/opt_customer/dm/
        partition_by: columns user want to partition, if None do not partition
        database : If user want to store to database must have database
        table_name: If user want to map data hdfs to table must have table_name
        """
        from pyspark.sql.functions import to_date, lit
        import re

        sparkDF = data
        if encrypt_columns:
            if keys_path:
                if self.check_keys_path_format(keys_path):
                    sparkDF = self.encrypt_column(sparkDF=sparkDF, table_name=table_name, column_names=encrypt_columns,
                                                  keys_path=keys_path)
            else:
                raise Exception("You must add parameters keys_path=")

                
        if '.parquet' in hdfs_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        import re
        pattern = re.compile('^hdfs://')
        is_hdfs = pattern.search(hdfs_path)
        if not is_hdfs and 'file:' not in hdfs_path:
            hdfs_path = 'hdfs://' + hdfs_path
            
        if partition_by:
            if partition_by in data.columns:
                import pyspark.sql.functions as F
                from pyspark.sql.functions import col
                check_date = sparkDF.select(F.length(col(partition_by))).distinct().collect()
                if check_date:
                    if 10 in list(check_date[0]):
                        sparkDF = sparkDF.withColumn(partition_by, to_date(partition_by))
            else:
                if not partition_date:
                    self.query_yes_no("""You should config partition_date, default today \nContinues Y/n?""")
                    from datetime import date
                    import datetime

                    today = date.today()
                    today = today.strftime("%Y-%m-%d")
                    partition_date = today

                # add constant column string ELT_DATE
                sparkDF = sparkDF.withColumn(partition_by, lit(partition_date))
                # convert string to date
                sparkDF = sparkDF.withColumn(partition_by, to_date(partition_by))

            print('HDFS path: ', hdfs_path)
            

                
            # if table exist compare datatype before store
            if self.check_is_file(hdfs_path):
                self.compare_data_type(self.read_first_file(database, table_name, hdfs_path), sparkDF)

            self.spark.sql("SET spark.sql.sources.partitionOverwriteMode = dynamic")

            if repartition and numPartitions:
                sparkDF.repartition(numPartitions).write.format(file_format).option('compression', compression).mode("overwrite").partitionBy(partition_by).option("path", hdfs_path).saveAsTable(database + '.' + table_name)
            elif repartition:
                numPartitions = self.num_repartition(sparkDF)
                sparkDF.repartition(numPartitions).write.format(file_format).option('compression', compression).mode("overwrite").partitionBy(partition_by).option("path", hdfs_path).saveAsTable(database + '.' + table_name)
            else:
                sparkDF.write.format(file_format).option('compression', compression).mode("overwrite").partitionBy(partition_by).option("path", hdfs_path).saveAsTable(
                    database + '.' + table_name)

        else:
            if repartition and numPartitions:
                sparkDF.repartition(numPartitions).write.format(file_format).mode("overwrite").option("path", hdfs_path).saveAsTable(database + '.' + table_name)
            elif repartition:
                numPartitions = self.num_repartition(sparkDF)
                sparkDF.repartition(numPartitions).write.format(file_format).mode("overwrite").option("path", hdfs_path).saveAsTable(database + '.' + table_name)
            else:
                sparkDF.write.format(file_format).mode("overwrite").option("path", hdfs_path).saveAsTable(database + '.' + table_name)
        
        self.spark.sql(f"""REFRESH TABLE {database}.{table_name}""")
        
        
        try:
            from spark_sdk.pylineage import addLineageAfterToDwh
            addLineageAfterToDwh(database+'.'+table_name)
        except Exception as e: 
            pass
        

    def to_dwh_spark(self, data, hdfs_path, repartition=False, numPartitions=None, partition_by='', partition_date='',compression='snappy',
                     database='', table_name='', encrypt_columns=[], keys_path=''):
        """
        Parameters
        ----------
        data: pandas dataframe
        hdfs_path : Path hdfs user want to store. EX: /data/fpt/ftel/cads/opt_customer/dm/
        partition_by: columns user want to partition, if None do not partition
        database : If user want to store to database must have database
        table_name: If user want to map data hdfs to table must have table_name
        """
        sparkDF = self.spark.createDataFrame(data)
        self.store_spark_dataframe_to_dwh(sparkDF, hdfs_path=hdfs_path, repartition=repartition,
                                          numPartitions=numPartitions, partition_by=partition_by,
                                          partition_date=partition_date, database=database, table_name=table_name,
                                          encrypt_columns=encrypt_columns, keys_path=keys_path, compression=compression)
        

        
    def read_csv(self, path, sep=',', header=True):
        return self.spark.read.option("header",header).options(delimiter=sep).csv(path)
        
    def read_parquet(self, path):
        return self.spark.read.parquet(path)
    
    def describe_table(self, full_table_name, to_pandas=False):
        if to_pandas:
            pd.set_option('max_colwidth', 300)
            return self.spark.sql(f"""DESCRIBE FORMATTED {full_table_name}""").toPandas()
        else:
            return self.spark.sql(f"""DESCRIBE FORMATTED {full_table_name}""").show(100, 200)
        
        
    def show_table(self, database, to_pandas=False):
        if to_pandas:
            pd.set_option('max_colwidth', 300)
            return self.spark.sql(f"""SHOW TABLES FROM {database}""").toPandas()
        else:
            return self.spark.sql(f"""SHOW TABLES FROM {database}""").show(100, 200)
        
    
    
    def stop(self):
        self.spark.stop()
        return True


class PyArrow:
    def __init__(self, existing_data_behavior='overwrite_or_ignore'):
        # Install latest Pyarrow version
        import os
        from spark_sdk.conf import (HADOOP_HOST, HADOOP_PORT)
        self.hdfs = fs.HadoopFileSystem(host=HADOOP_HOST, port=HADOOP_PORT)
        self.existing_data_behavior = existing_data_behavior
        
    def check_keys_path_format(self, keys_path):
        import re
        if re.search('json$', keys_path):
            return True
        else:
            raise Exception("keys_path must end with '.json'")

    def autogenerate_key(self, length_key=22):
        import string
        import random

        key = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length_key))
        key = key + "=="
        return key

    
    def read_json(self, path):
        with self.hdfs.open_input_file(path) as file:
            return json.load(file)
        
    def write_json(self, data, path):
        with self.hdfs.open_output_stream(path) as file:
            json.dump(data, Utf8Encoder(file))
    
    def append_keys_to_file(self, table_name, column_name='', keys_path='keys.json'):
        from datetime import datetime
        import json

        if self.check_is_file(keys_path):
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        c = column_name
        keys = {}

        keys["name"] = f"secret_for_{table_name}_{c}"
        keys["description"] = ""
        keys["created"] = round(datetime.timestamp(datetime.now()))
        keys["material"] = self.autogenerate_key()
        list_keys.append(keys)

        with self.hdfs.open_output_stream(keys_path) as file:
            json.dump(list_keys, Utf8Encoder(file))

    def auto_generate_list_keys(self, table_name, column_name='', keys_path='keys.json'):
        from datetime import datetime
        import json

        if self.check_is_file(keys_path):
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        for c in column_name.split(','):
            if c:
                keys = {}

                keys["name"] = f"secret_for_{table_name}_{c}"
                keys["description"] = f"This is secret_for_{table_name}_{c}"
                keys["created"] = round(datetime.timestamp(datetime.now()))
                keys["material"] = self.autogenerate_key()

                list_keys.append(keys)
        return list_keys
            
    def encrypt_column(self, data, table_name, column_names=[], keys_path=''):
        # check file keys exist
        if self.check_is_file(keys_path):
            # Opening JSON file
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        keys_exist = {}
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            # check if key in file
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]

        for c in column_names:
            # if not found key generate new key append to keys.json
            if c not in keys_exist.keys():
                print('Append key for', c)
                self.append_keys_to_file(table_name, c, keys_path)

        list_keys = self.read_json(keys_path)
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]
                   
        from .pandas_decrypt import encrypt_column
        for c in column_names:
            data[c] = data[c].encrypt_column(keys_exist[c])
        
        return data
    
    
    def pandas_to_parquet(self, pandas_type):
        TYPE_MAPPER = {
            'object': 'STRING',
            'float64': 'DOUBLE',
            'float32': 'DOUBLE',
            'int64': 'INT64',
            'int32': 'INT32',
            'bool': 'BOOLEAN',
            'datetime64': 'timestamp[s]',
            'datetime64[ns]': 'timestamp[s]',
            'datetime64[ns, Asia/Jakarta]': 'timestamp[s]',
            'datetime64[ns, UTC]': 'timestamp[s]'
        }

        return TYPE_MAPPER.get(pandas_type, 'None')

    def _check_series_convert_column_pyarrow(self, data, partition_by):
        
        new_type = {}
        
        # check column duplicated
        if contains_duplicates(data.columns):
            print("Columns is duplicated, check your data ")
        
        for c in data.columns:
            if str(data[c].dtype) == 'category':
                if max(data[c].str.len()) ==  min(data[c].str.len()):
                    data[c] = pd.to_datetime(data[c])
            if c == partition_by:
                new_type[partition_by] = pa.date64()
            else:

                data[c] = _check_series_convert_timestamps_internal(data[c], timezone=None)
                new_type[c] = self.pandas_to_parquet(str(data[c].dtype))

        fields = [pa.field(x, y) for x, y in new_type.items()]
        new_schema = pa.schema(fields)
        table = pa.Table.from_pandas(
            data,
            schema=new_schema,
            preserve_index=False
        )

        return table

    def check_is_file(self, hdfs_path):
        check = self.hdfs.get_file_info(hdfs_path)
        if check.type._name_ in ["Directory", "File"]:
            return True
        else:
            return False
        
    def read_table(self, source, filters=''):
        if filters:
            return pq.read_table(source=source, filters=filters, filesystem=self.hdfs)
        else:
            return pq.read_table(source=source, filesystem=self.hdfs)
    
    
    def read_first_file(self, hdfs_path):
        '''
        Read schema pyarrow
        '''
        first_hdfs = pa.HadoopFileSystem().ls(hdfs_path)[-1]
        return self.read_table(source=first_hdfs)

                   
    def compare_data_type(self, first_sparkDF, second_sparkDF, partition_by):
        """
        Function to check when write data second time
        """
        error = {}
        first_sparkDF_schema = {}
        second_sparkDF_schema = {}
        
        for c in first_sparkDF.schema:
            c_name = c.name
            if partition_by == c_name and partition_by != '':
                continue
            first_sparkDF_schema[c.name] = c.type
            
        for c in second_sparkDF.schema:
            c_name = c.name
            if partition_by == c_name and partition_by != '':
                continue
            second_sparkDF_schema[c.name] = c.type

        if len(first_sparkDF_schema.keys()) != len(second_sparkDF_schema.keys()):
            print(f'First time have columns', first_sparkDF.schema.names)
            print(f'Second time have columns', second_sparkDF.schema.names)
            
            raise ValueError(f"First time have {len(first_sparkDF)} columns but second time have {len(second_sparkDF.schema)} columns")
            
        for c in second_sparkDF_schema.keys():  
            second_type = second_sparkDF_schema[c]
            first_type = first_sparkDF_schema[c]

            if first_type != second_type:
                error[c] = {'first_time': first_type, 'second_time': second_type}

            if error.keys():
                print('Error', error)
                del first_sparkDF
                del second_sparkDF
                raise TypeError(f"DataType of Columns this time store is not like first time")
        print('Check schema OK')
        del first_sparkDF

        
    def to_dwh_pyarrow(self, data, hdfs_path, database, table_name, partition_by='', partition_date='',
                       use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore',encrypt_columns=[], keys_path=''):
        
        if encrypt_columns:
            if keys_path:
                if self.check_keys_path_format(keys_path):
                    data = self.encrypt_column(data=data, table_name=table_name, column_names=encrypt_columns, keys_path=keys_path)
            else:
                raise Exception("You must add parameters keys_path=")
                
                
        if partition_by:
            if partition_by in data.columns:
                table = self._check_series_convert_column_pyarrow(data, partition_by)
            else:
                if not partition_date:
                    from datetime import date
                    import datetime

                    today = date.today()
                    today = today.strftime("%Y-%m-%d")
                    partition_date = today

                data[partition_by] = pd.to_datetime(partition_date)
                table = self._check_series_convert_column_pyarrow(data, partition_by)

            print('HDFS path: ', hdfs_path)

            if self.check_is_file(hdfs_path):
                self.compare_data_type(self.read_first_file(hdfs_path), table, partition_by)

            pq.write_to_dataset(
                table,
                root_path=hdfs_path,
                partition_cols=[partition_by],
                use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
                filesystem=self.hdfs,
                existing_data_behavior=existing_data_behavior
            )

        else:
            table = self._check_series_convert_column_pyarrow(data, partition_by='')
            pq.write_to_dataset(
                table,
                root_path=hdfs_path,
                use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
                filesystem=self.hdfs,
                existing_data_behavior=existing_data_behavior
            )

        PySpark(driver_memory='1g', num_executors='1', executor_memory='1G').create_table_and_metadata(
            database=database, table_name=table_name, partition_by=partition_by, hdfs_path=hdfs_path)
        
        PySpark(driver_memory='1g', num_executors='1', executor_memory='1G').spark.sql(f"""REFRESH TABLE {database}.{table_name}""")
        

        

        
######################
def read_table(full_table_name, engine='spark',
              driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False):
    PS = PySpark(driver_memory=driver_memory, executor_memory=executor_memory, num_executors=num_executors, port=port, yarn=yarn)
    return PS.spark.sql(f"select * from {full_table_name}")



def sql(query, driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False):
    PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
    return PS.spark.sql(query)

def refresh_table(full_table_name, driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False):
    PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
    return PS.spark.sql(f"""REFRESH TABLE {full_table_name}""")


def read_dwh_pd(full_table_name, filters='', engine='spark', driver_memory='8G', num_executors='4', executor_memory='4G', port='', yarn=False):
    # ========================LINEAGE======================
    try:
        from spark_sdk.pylineage import emitPythonJob
        emitPythonJob(full_table_name = full_table_name, outputNode=False)
    except:
        pass
    # =====================================================
    if engine == 'pyarrow':
        df_arrow = PyArrow().read_table(source=get_location_from_table(full_table_name), filters=render_filters_pyarrow(filters))
        df = df_arrow.to_pandas()
            
    if engine == 'spark':
        PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
        if filters:
            filters = 'where ' + filters
        
        
        df_spark = PS.spark.sql(f"select * from {full_table_name} {filters}")
        df = df_spark.toPandas()
    return df

def read_dwh(full_table_name, filters='', engine='spark', driver_memory='8G', num_executors='4', executor_memory='4G', port='', yarn=False):
    PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
    if filters:
        filters = 'where ' + filters
    df_spark = PS.spark.sql(f"select * from {full_table_name} {filters}")
    return df_spark


    
def read_csv(path, sep=',', header=True,
           driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False,
           engine='spark',
           use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore'):
    PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
    return PS.read_csv(path=path, sep=sep, header=header)


def read_parquet(path,
           driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False,
           engine='spark',
           use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore'):

    PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
    return PS.read_parquet(path=path)


def read_json(path,
           driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False,
           engine='pyarrow',
           use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore'):
    return PyArrow().read_json(path)


def write_json(data, path,
           driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False,
           engine='pyarrow',
           use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore'):
    # ========================LINEAGE======================
    try:
        from spark_sdk.pylineage import emitPythonJob
        emitPythonJob(hdfs_path = path, outputNode=True)
    except:
        pass
    # =====================================================
    return PyArrow().write_json(data = data, path = path)


def spark_dataframe_to_dwh(self, hdfs_path, database, table_name, repartition=False, numPartitions=None, partition_by='',
           partition_date='', compression='snappy', encrypt_columns=[], keys_path='',
           driver_memory='8G', executor_memory='5g', num_executors='1', parallel=True, port='', yarn=False
           ):

    PySpark(driver_memory=driver_memory, executor_memory=executor_memory, num_executors=num_executors, port=port,
            yarn=yarn).store_spark_dataframe_to_dwh(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name, 
                                                    repartition=repartition, numPartitions=numPartitions, partition_by=partition_by, partition_date=partition_date, compression=compression,
                                                    encrypt_columns=encrypt_columns, keys_path=keys_path)
    
    
def to_dwh(self, hdfs_path, database, table_name, repartition=False, numPartitions=None, compression = 'snappy', partition_by='',
           partition_date='', encrypt_columns=[], keys_path='',
           driver_memory='8G', executor_memory='4g', num_executors='1', parallel=True, port='', yarn=False,
           engine='spark',
           use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore'):
    
    if repartition:
        engine='spark'
    
    df_memory = self.memory_usage(index=True).sum() / 1024 / 1024


    if engine == 'spark' or 'delta' in hdfs_path.lower():
        if parallel:
            num_executors = choose_num_core(df_memory)

        driver_memory = choose_driver_memory(df_memory)
        executor_memory = choose_executor_memory(df_memory, int(num_executors))

        PySpark(driver_memory=driver_memory, executor_memory=executor_memory, num_executors=num_executors, port=port,
                yarn=yarn).to_dwh_spark(data=self, hdfs_path=hdfs_path, repartition=repartition,
                                        numPartitions=numPartitions, partition_by=partition_by,
                                        partition_date=partition_date, compression=compression, database=database, table_name=table_name,
                                        encrypt_columns=encrypt_columns, keys_path=keys_path)
    else:
        PyArrow().to_dwh_pyarrow(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name,
                                 partition_by=partition_by, partition_date=partition_date,
                                 use_deprecated_int96_timestamps=True, existing_data_behavior=existing_data_behavior, encrypt_columns=encrypt_columns, keys_path=keys_path)

def drop_table(full_table_name, engine='spark', yarn=False):
    PS = PySpark(driver_memory='1G', num_executors='1', executor_memory='1G', yarn=yarn)
    if PS.query_yes_no("Are you sure you want to drop table?", default='no'):
        provider = get_provider_from_table(full_table_name)
        if provider != 'delta':
            PS.spark.sql(f"""ALTER TABLE {full_table_name} SET TBLPROPERTIES('external.table.purge' = 'false')""")
        PS.spark.sql(f"DROP TABLE {full_table_name}")


def drop_table_and_delete_data(full_table_name, yarn=False):
    PS = PySpark(driver_memory='1G', num_executors='1', executor_memory='1G', yarn=yarn)
    if PS.query_yes_no("Are you sure you want to drop table and delete data?", default='no'):
        provider = get_provider_from_table(full_table_name)
        if provider == 'delta':
            import pandas as pd

            df = PS.spark.sql(f"DESCRIBE FORMATTED {full_table_name}").toPandas()
            location = df[df['col_name']=='Location']['data_type'].values[0]

            print(f"MOVE DATA {location} to /shared/trash")
            base_name = os.path.basename(location)
            if exists(f"/shared/trash/{base_name}"):
                os.system(f"hdfs dfs -rm -r /shared/trash/{base_name}")
            os.system(f"hdfs dfs -mv {location} /shared/trash")
            PS.spark.sql(f"DROP TABLE {full_table_name}")
        else:
            import pandas as pd

            df = PS.spark.sql(f"DESCRIBE FORMATTED {full_table_name}").toPandas()
            location = df[df['col_name']=='Location']['data_type'].values[0]

            print(f"MOVE DATE {location} to /shared/trash")
            base_name = os.path.basename(location)
            if exists(f"/shared/trash/{base_name}"):
                os.system(f"hdfs dfs -rm -r /shared/trash/{base_name}")
            os.system(f"hdfs dfs -mv {location} /shared/trash")
            PS.spark.sql(f"""ALTER TABLE {full_table_name} SET TBLPROPERTIES('external.table.purge' = 'false')""")
            PS.spark.sql(f"DROP TABLE {full_table_name}")

        
###############
def ls(path, detail=False):
    if "file:" in path:
        import os
        return os.listdir(path.replace('file:', ''))
    else:
        return pa.HadoopFileSystem().ls(path, detail=detail)


def mkdir(path):
    return pa.HadoopFileSystem().mkdir(path)


def cat(path):
    return pa.HadoopFileSystem().cat(path)


def exists(path):
    if "file:" in path:
        import os
        return os.path.exists(path.replace('file:', ''))
    else:
        return pa.HadoopFileSystem().exists(path)    


def info(path):
    return pa.HadoopFileSystem().info(path) 


def open(path, mode='rb'):
    return pa.HadoopFileSystem().open(path, mode=mode)


def show(self, n: int = 20, truncate: Union[bool, int] = 50, vertical: bool = False) -> None:
    """Prints the first ``n`` rows to the console.
    .. versionadded:: 1.3.0
    Parameters
    ----------
    n : int, optional
        Number of rows to show.
    truncate : bool or int, optional
        If set to ``True``, truncate strings longer than 20 chars by default.
        If set to a number greater than one, truncates long strings to length ``truncate``
        and align cells right.
    vertical : bool, optional
        If set to ``True``, print output rows vertically (one line
        per column value).
    Examples
    --------
    >>> df
    DataFrame[age: int, name: string]
    >>> df.show()
    +---+-----+
    |age| name|
    +---+-----+
    |  2|Alice|
    |  5|  Bob|
    +---+-----+
    >>> df.show(truncate=3)
    +---+----+
    |age|name|
    +---+----+
    |  2| Ali|
    |  5| Bob|
    +---+----+
    >>> df.show(vertical=True)
    -RECORD 0-----
     age  | 2
     name | Alice
    -RECORD 1-----
     age  | 5
     name | Bob
    """

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Parameter 'n' (number of rows) must be an int")

    if not isinstance(vertical, bool):
        raise TypeError("Parameter 'vertical' must be a bool")

    if isinstance(truncate, bool) and truncate:
        print(self._jdf.showString(n, 20, vertical))
    else:
        try:
            int_truncate = int(truncate)
        except ValueError:
            raise TypeError(
                "Parameter 'truncate={}' should be either bool or int.".format(truncate)
            )

        print(self._jdf.showString(n, int_truncate, vertical))
        
### dataframe function
def spark_dataframe_info(self, driver_memory='8G', num_executors='4', executor_memory='4G', parallel=True, port='', yarn=False):
    sdf = self
    sdf.createOrReplaceTempView('info_table')
    sql = ''
    
    column_names = sdf.schema.names
    
    if len(column_names) > 1:
        
        for c in column_names[:-1]:
            check_column = f"""
                SELECT '{c}' column,
                count(case when {c} is null or {c} is not null then 1 end) total_count, 
                count(case when {c} is null then 1 end) is_null_count,
                CONCAT(CAST(ROUND(count(case when {c} is null then 1 end) / count(case when {c} is not null or {c} is null then 1 end) * 100, 2) as STRING), '%') percent_isnull FROM info_table \n"""
            sql += check_column
            sql += 'UNION ALL \n'
    
    c=column_names[-1]
    check_column_end = f"""
                SELECT '{c}' column,
                count(case when {c} is null or {c} is not null then 1 end) total_count, 
                count(case when {c} is null then 1 end) is_null_count,
                CONCAT(CAST(ROUND(count(case when {c} is null then 1 end) / count(case when {c} is not null or {c} is null then 1 end)* 100, 2) as STRING), '%') percent_isnull FROM info_table \n"""
    sql += check_column_end
    PS = PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, port=port, yarn=yarn)
    return PS.spark.sql(sql)


def limit_timestamp(sparkDF):
    sql = ""
    for c in sparkDF.schema:
        if str(c.dataType) in ['TimestampType()', 'DateType()']:
            sql += f"AND {c.name} between '1900-01-01' AND '2300-01-01' \n"
    PS = PySpark()
    print("Filter")
    print(sql)
    sparkDF.createOrReplaceTempView('df')
    return PS.spark.sql(f"""SELECT * FROM df WHERE 1=1 {sql}""")


############ other table functions 
def get_location_from_table(full_table_name):
    from spark_sdk import HIVE_IP_NODE1,HIVE_IP_NODE2 
    HIVE = HiveMetastoreClient(hmss_ro_addrs=[HIVE_IP_NODE1,HIVE_IP_NODE2])
    d, t = full_table_name.split('.')

    location = HIVE.get_table(db_name=d, tb_name=t).__dict__['sd'].__dict__['location']
    import re

    pattern = re.compile('/data/')
    x = pattern.search(location)

    location = location[x.start():]
    return location

def get_provider_from_table(full_table_name):
    HIVE = HiveMetastoreClient(hmss_ro_addrs=["master01-dc9c14u40.bigdata.local:9083","master02-dc9c14u41.bigdata.local:9083"])
    d, t = full_table_name.split('.')

    return HIVE.get_table(db_name=d, tb_name=t).parameters['spark.sql.sources.provider']


def render_filters_pyarrow(sql):
    """
    function support read_dwh() by pyarrow engine, render sql where clause
    """
    if sql:
        import sqlglot
        sql = sqlglot.transpile(sql, write='spark', identify=True, pretty=True)[0]
        list_bool_expression = sql.split('\n')


        import re

        pattern_column = re.compile('`(.*?)`')
        pattern_operator = re.compile('[<>=]')


        list_filters = []
        for b in list_bool_expression:
            x1 = pattern_column.search(b)
            column_name = b[x1.start()+1: x1.end()-1]

            x2 = pattern_operator.search(b)
            operator = b[x2.start(): x2.end()]

            value = b[x2.end()+2: -1]

            list_filters.append((column_name, operator, value))

        return list_filters
    else:
        return ''
