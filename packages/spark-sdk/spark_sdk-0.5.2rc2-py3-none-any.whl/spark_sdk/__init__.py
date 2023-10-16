from .pyspark_add_on import PySpark, PyArrow, Utf8Encoder
from .pyspark_add_on import to_dwh, drop_table, drop_table_and_delete_data, read_table, sql, refresh_table, spark_dataframe_to_dwh
from .pyspark_add_on import ls, mkdir, cat, exists, info, open
from .pyspark_add_on import read_dwh_pd, read_csv, read_json, write_json, read_parquet, read_dwh
from .pyspark_add_on import show, refresh_table
from .pyspark_add_on import limit_timestamp
from .pyspark_add_on import spark_dataframe_info
from .create_yaml_file import CreateYamlDWH
from .pandas_decrypt import decrypt, decrypt_column


try:
    from IPython import get_ipython
    from .magics import *
    load_ipython_extension(get_ipython())
except:
    pass


from .utils import modulereload, choose_num_core
from pandas.core.series import Series


import pandas as pd
from pandas import DataFrame


DataFrame.to_dwh = to_dwh
#DataFrame._repr_html_ = PandasDataFrame_repr_html_
modulereload(pd)

Series.decrypt_column = decrypt_column
pd.read_dwh = read_dwh_pd
modulereload(pd)


from pyspark.sql import DataFrame as SparkDataFrame
SparkDataFrame.to_dwh = spark_dataframe_to_dwh
SparkDataFrame.info = spark_dataframe_info

try:
    from spark_sdk.pylineage import PandasConversionMixin
    SparkDataFrame.toPandas = PandasConversionMixin.toPandasLineage
except:
    pass


SparkDataFrame.show = show

__version__ = '0.5.2rc2'
__all__ = ["PySpark", "PyArrow"]


