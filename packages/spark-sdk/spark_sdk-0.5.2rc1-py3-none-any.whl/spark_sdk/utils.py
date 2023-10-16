def modulereload(modulename):
    import importlib
    importlib.reload(modulename)
    
    
def choose_driver_memory(mb):
    x = int(mb // 64 + 1)
    if x <= 1:
        x = 1
    if x >= 20:
        x = 20
    print('driver-memory', str(x) + 'g')
    return str(x) + 'g'


def choose_num_core(mb):
    x = int(mb // 256 + 1)
    if x <= 1:
        x = 1
    if x >= 8:
        x = 8
    print('cores', x)
    return str(x)


def choose_executor_memory(mb, cores):
    x = int(mb // 64 / cores + 1)
    if x <= 1:
        x = 1
    if x >= 12:
        x = 12
    print('executor-memory', str(x) + 'g')
    return str(x) + 'g'


def _check_series_convert_timestamps_internal(s, timezone):
    """
    Convert a tz-naive timestamp in the specified timezone or local timezone to UTC normalized for
    Spark internal storage

    Parameters
    ----------
    s : pandas.Series
    timezone : str
        the timezone to convert. if None then use local timezone

    Returns
    -------
    pandas.Series
        `pandas.Series` where if it is a timestamp, has been UTC normalized without a time zone
    """
    from pyspark.sql.pandas.utils import require_minimum_pandas_version
    require_minimum_pandas_version()

    from pandas.api.types import is_datetime64_dtype, is_datetime64tz_dtype
    # TODO: handle nested timestamps, such as ArrayType(TimestampType())?
    if is_datetime64_dtype(s.dtype):
        # When tz_localize a tz-naive timestamp, the result is ambiguous if the tz-naive
        # timestamp is during the hour when the clock is adjusted backward during due to
        # daylight saving time (dst).
        # E.g., for America/New_York, the clock is adjusted backward on 2015-11-01 2:00 to
        # 2015-11-01 1:00 from dst-time to standard time, and therefore, when tz_localize
        # a tz-naive timestamp 2015-11-01 1:30 with America/New_York timezone, it can be either
        # dst time (2015-01-01 1:30-0400) or standard time (2015-11-01 1:30-0500).
        #
        # Here we explicit choose to use standard time. This matches the default behavior of
        # pytz.
        #
        # Here are some code to help understand this behavior:
        # >>> import datetime
        # >>> import pandas as pd
        # >>> import pytz
        # >>>
        # >>> t = datetime.datetime(2015, 11, 1, 1, 30)
        # >>> ts = pd.Series([t])
        # >>> tz = pytz.timezone('America/New_York')
        # >>>
        # >>> ts.dt.tz_localize(tz, ambiguous=True)
        # 0   2015-11-01 01:30:00-04:00
        # dtype: datetime64[ns, America/New_York]
        # >>>
        # >>> ts.dt.tz_localize(tz, ambiguous=False)
        # 0   2015-11-01 01:30:00-05:00
        # dtype: datetime64[ns, America/New_York]
        # >>>
        # >>> str(tz.localize(t))
        # '2015-11-01 01:30:00-05:00'
        tz = timezone or _get_local_timezone()
        return s.dt.tz_localize(tz, ambiguous=False).dt.tz_convert('UTC')
    elif is_datetime64tz_dtype(s.dtype):
        return s.dt.tz_convert('UTC')
    else:
        return s
    
    
def _get_local_timezone():
    """ Get local timezone using pytz with environment variable, or dateutil.

    If there is a 'TZ' environment variable, pass it to pandas to use pytz and use it as timezone
    string, otherwise use the special word 'dateutil/:' which means that pandas uses dateutil and
    it reads system configuration to know the system local timezone.

    See also:
    - https://github.com/pandas-dev/pandas/blob/0.19.x/pandas/tslib.pyx#L1753
    - https://github.com/dateutil/dateutil/blob/2.6.1/dateutil/tz/tz.py#L1338
    """
    import os
    return os.environ.get('TZ', 'dateutil/:')

def contains_duplicates(X):
    import numpy as np
    return len(np.unique(X)) != len(X)


def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        import os
        import pip
        os.environ['http_proxy'] = "http://proxy.hcm.fpt.vn:80" 
        os.environ['https_proxy'] = "http://proxy.hcm.fpt.vn:80"
        pip.main(['install', package])
        modulereload(__import__(package))