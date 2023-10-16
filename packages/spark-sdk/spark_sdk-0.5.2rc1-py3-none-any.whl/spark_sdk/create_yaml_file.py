import pandas as pd
import os
import re
import argparse
import sys


class CreateYamlDWH:
    def __init__(self, csv_file, hdfs_path, database_name, table_name, sep, yaml_path):
        '''
        from spark_sdk.create_yaml_file import CreateYamlDWH
        create_yaml = CreateYamlDWH(
        csv_file = '/bigdata/user_profile/api/api_getdata_daily/api_getdata_daily_2022-08-12.csv',
        sep = '\t',
        hdfs_path = '/data/fpt/ftel/insights/dwh/',
        database_name = 'ftel_dwh_insights',
        table_name = 'scd_customer_insight_daily',
        yaml_path = 'user/profile/metorikku/hive/'
        )
        '''
        self.file = csv_file
        self.hdfs_path = hdfs_path
        self.name = table_name
        self.database_name = database_name
        self.sep = sep
        self.yaml_path = yaml_path


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


    def generate_sql(self, input_file, sep):
        check_file = re.findall('(\d\d\d\d-\d\d-\d\d|\d\d\d\d-\d\d)', input_file)[0]
        if len(check_file) == 10:
            period = 'daily'
            partition = 'date("${elt_date}") d,'
            partition_col = 'd'
            input_path = re.sub(check_file, '${elt_date}', input_file)
            elt_date = '{elt_date}'
        else:
            period = 'monthly'
            partition = 'date("${PREV_MONTH}-01") m'
            partition_col = 'm'
            input_path = re.sub(check_file, '${PREV_MONTH}', input_file)
            elt_date = '{PREV_MONTH}'

        df = pd.read_csv(input_file, sep=sep, nrows=100)

        fields = "\n                "
        comma = ",\n                "
        for c in df.columns:
            name = c
            last_pos = 0

            i = 0
            for letter in name:
                if letter.isupper():
                    if i - last_pos > 1:
                        name = name[:i] + "_" + name[i:]
                        i += 1
                    last_pos = i
                if letter.islower() and i - last_pos == 1:
                    if name[i-2:i-1] != '_' and name[i-2:i-1].isupper():
                        name = name[:i-1] + '_' + name[i-1:] 
                        i += 1
                i += 1

            new_name = name.lower()
            parquet_type = self.pandas_to_parquet(str(df[c].dtype))
            field_dev = f"CAST({c} as {parquet_type}) as {new_name}{comma}"
            fields += field_dev


        table_name = '{table_name}'
        sql = f'''
            SELECT
                    {fields}
                {partition}
            FROM ${table_name}
        '''

        return input_path, sep, sql, elt_date, partition_col


    def combine_yaml_file(self, input_path, sep, sql, elt_date, partition_col):
        table_name = '{table_name}'

        yaml_file = f"""
metrics:
  - |
    steps:
      - dataFrameName: outputdata
        sql: |-
            {sql}

    output:
      - dataFrameName: outputdata
        outputType: File
        format: parquet
        name: {self.database_name.upper()}
        outputOptions:
          saveMode: Overwrite
          path: ${table_name}.parquet
          tableName: {self.database_name}.${table_name}
          partitionBy:
              - {partition_col}
inputs:
  ${table_name}:
    file:
      path: file://{input_path}
      format: csv
      options:
        header: true
        sep: "{sep}"

outputs:
  {self.database_name.upper()}:
    file:
      dir: hdfs://{self.hdfs_path}
logLevel: ERROR
explain: true
    """
        return yaml_file


    def generate_yaml_file(self):
        input_path, sep, sql, elt_date, partition_col = self.generate_sql(self.file, self.sep)
        yaml_file = self.combine_yaml_file(input_path, sep, sql, elt_date, partition_col)
        print(yaml_file)

        print("####################################################################")
        print("Create File as:", self.name)

        with open(f'{self.name}.yaml', "w") as f:
            f.write(yaml_file)
        
 