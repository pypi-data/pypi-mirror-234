import numbers
import pytz
import traceback
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta, timezone
from qtc.consts.enums import DateDataType
from qtc.ext.logging import set_logger
logger = set_logger()


DEFAULT_TIME_ZONE = 'America/New_York'


def datetime_to_dateid(date):
    """
    :param date: Date in datetime type.
    :type date: datetime
    :return: int - Date in '%Y%m%d' format.

    >>> from datetime import datetime
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.datetime_to_dateid(datetime(2019, 9, 25))
    20190925
    >>> adt_utc = datetime(2020, 8, 7, 2, 0, 0, tzinfo=pytz.UTC)
    >>> adt_ny = adt_utc.astimezone(pytz.timezone('America/New_York'))
    >>> dtu.datetime_to_dateid(adt_utc)
    20200807
    >>> dtu.datetime_to_dateid(adt_ny)
    20200806
    """
    formatted_date = date.strftime('%Y%m%d %Z')[:8]
    return int(formatted_date)


def dateid_to_datetime(dateid, timezone=None):
    """
    :param dateid: Date in '%Y%m%d' format.
    :type dateid: int
    :return: datetime - Date in datetime type.

    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.dateid_to_datetime(20190925)
    datetime.datetime(2019, 9, 25, 0, 0)
    """
    dt = datetime.strptime(str(dateid), '%Y%m%d')
    if timezone is not None:
        # dt = pytz.timezone(timezone).localize(dt)
        dt = dt.replace(tzinfo=pytz.timezone(timezone))

    return dt


def dateid_to_datestr(dateid, sep='-'):
    """
    :param dateid: Date in '%Y%m%d' format.
    :type dateid: int
    :param sep: Separator in the returned date str.
    :type date: int
    :return: str - Date in f"%Y{sep}%m{sep}%d" format.

    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.dateid_to_datestr(20190925)
    '2019-09-25'
    >>> dtu.dateid_to_datestr(20191013, sep='/')
    '2019/10/13'
    """
    dateid = str(dateid)
    date_str = f"{dateid[0:4]}{sep}{dateid[4:6]}{sep}{dateid[6:8]}"
    return date_str


def curr_dateid(timezone=None):
    """
    :return: int - TODAY in '%Y%m%d' format.

    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.curr_dateid()
    """
    today = datetime.now() if timezone is None else datetime.now(pytz.timezone(timezone))
    return datetime_to_dateid(today)


def is_weekday(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.is_weekday(20200511)
    True
    >>> dtu.is_weekday(20200516)
    False
    """

    if isinstance(date, int):
        date = dateid_to_datetime(date)
    elif not isinstance(date, datetime):
        raise Exception(f"Supported date types are [dateid | datetime] !")

    return date.weekday() not in [5, 6]


def get_biz_dateids(start_date, end_date):
    bdates = pd.bdate_range(dateid_to_datestr(dateid=normalize_date_to_dateid(date=start_date), sep='-'),
                            dateid_to_datestr(dateid=normalize_date_to_dateid(date=end_date), sep='-')).strftime('%Y%m%d')
    return [int(date) for date in bdates]


def prev_biz_dateid(dateid):
    one_day = timedelta(days=1)
    prev_day = dateid_to_datetime(dateid) - one_day
    while not is_weekday(prev_day):
        prev_day -= one_day

    return datetime_to_dateid(prev_day)


def next_biz_dateid(dateid):
    one_day = timedelta(days=1)
    next_day = dateid_to_datetime(dateid) + one_day
    while not is_weekday(next_day):
        next_day += one_day

    return datetime_to_dateid(next_day)


def parse_datetime(dt, format=None, timezone=None, ret_as_timestamp=False):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.parse_datetime(20200210)
    datetime.datetime(2020, 2, 10, 0, 0)
    >>> dtu.parse_datetime('2020-02-10', ret_timestamp=True)
    Timestamp('2020-02-10 00:00:00')
    >>> dtu.parse_datetime('20200210-164523', timezone='US/Eastern')
    datetime.datetime(2020, 2, 10, 16, 45, 23, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    >>> dtu.parse_datetime('2020/02/10 16:45:23', format='%Y/%m/%d %H:%M:%S', timezone='Asia/Shanghai')
    datetime.datetime(2020, 2, 10, 16, 45, 23, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
    >>> dtu.parse_datetime('2020-08-06', timezone=pytz.timezone('Europe/London'))
    datetime.datetime(2020, 8, 6, 0, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
    """

    if isinstance(dt, numbers.Integral):
        dt = str(dt)

    if (isinstance(dt, datetime) and not ret_as_timestamp) or \
            (isinstance(dt, pd.Timestamp) and ret_as_timestamp):
        return dt

    try:
        dt = pd.Timestamp(dt)
        if timezone is not None:
            dt = dt.tz_localize(timezone)

    except Exception as e:
        pass

    if isinstance(dt, pd.Timestamp):
        return dt if ret_as_timestamp else dt.to_pydatetime()

    if isinstance(dt, str):
        dt = pd.to_datetime(dt, format=format)
        if timezone is not None:
            dt = dt.tz_localize(timezone)

        return dt if ret_as_timestamp else dt.to_pydatetime()

    raise Exception(f"'dt' has to be of type [dateid | str | datetime | pd.Timestamp | np.datetime64] !")


def normalize_date_to_dateid(date=None):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.normalize_date_to_dateid(date=20210929)
    20210929
    >>> dtu.normalize_date_to_dateid(date='2021-09-29')
    20210929
    >>> dtu.normalize_date_to_dateid(datetime(2021,9,29))
    20210929
    """

    if date is None:
        return curr_dateid()

    return datetime_to_dateid(parse_datetime(date))


def convert_data_type_for_date_col(df, date_col=None,
                                   from_data_type=DateDataType.DATEID, to_data_type=DateDataType.TIMESTAMP,
                                   to_date_col_idx=None):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.convert_data_type_for_date_col(pd.DataFrame({'DateId':[20210927,20210928,20210929]}), date_col='DateId')
         DateId       Date
    0  20210927 2021-09-27
    1  20210928 2021-09-28
    2  20210929 2021-09-29
    """

    if isinstance(from_data_type, str):
        from_data_type = DateDataType.retrieve(from_data_type)

    if not isinstance(from_data_type, DateDataType):
        raise Exception(f"type(from_data_type)={type(from_data_type)} is not supported in [str|DateDataType] !")

    if isinstance(to_data_type, str):
        to_data_type = DateDataType.retrieve(to_data_type)

    if not isinstance(to_data_type, DateDataType):
        raise Exception(f"type(to_data_type)={type(to_data_type)} is not supported in [str|DateDataType] !")

    if from_data_type==to_data_type:
        # logger.warn(f'Skipping since from_data_type={from_data_type} is the same as to_data_type={to_data_type} !')
        return df

    if date_col is None:
        date_col = from_data_type.value

    if to_date_col_idx is None:
        to_date_col_idx = list(df.columns).index(date_col)+1

    from_date_col_keyword = from_data_type.value
    if 'DateTime' in date_col and (from_data_type==DateDataType.TIMESTAMP or from_data_type==DateDataType.DATETIME):
        from_date_col_keyword = 'DateTime'
    to_date_col = date_col.replace(from_date_col_keyword, to_data_type.value)

    if to_date_col in df.columns:
        df = df.drop(columns=[to_date_col])
        logger.warn(f'Column to_date_col={to_date_col} found in df and dropped !')
        to_date_col_idx -= 1

    if to_data_type==DateDataType.TIMESTAMP:
        if from_data_type==DateDataType.DATEID:
            new_dates = pd.to_datetime(df[date_col], format='%Y%m%d')
        else:
            new_dates = pd.to_datetime(df[date_col])
    elif to_data_type==DateDataType.DATEID:
        if from_data_type==DateDataType.TIMESTAMP:
            new_dates = [int(date) for date in df[date_col].dt.strftime('%Y%m%d')]
        else:
            raise Exception(f'{from_data_type} -> {to_data_type} not implemented yet!')
    else:
        raise Exception(f'{from_data_type} -> {to_data_type} not implemented yet!')

    df = df.copy()
    df.insert(to_date_col_idx, to_date_col, new_dates)
    return df


def normalize_dt(dt=None, timezone=None):
    if timezone is not None:
        if isinstance(timezone, str):
            timezone = pytz.timezone(timezone)

    if dt is None:
        dt = datetime.now() if timezone is None else datetime.now(tz=timezone)

    try:
        if isinstance(dt, str) or isinstance(dt, int):
            dt = parse_datetime(dt=dt, ret_as_timestamp=False, timezone=timezone)
        elif isinstance(dt, pd.Timestamp):
            if timezone is not None:
                dt = dt.tz_localize(timezone)
        elif isinstance(dt, datetime):
            if timezone is not None:
                dt = dt.astimezone(timezone)
    except Exception as e:
        logger.error(f"dt={dt} cannot be recognized as a datetime !")
        traceback.print_exc()
        return None

    return dt


def get_month_end(date):
    date = parse_datetime(dt=date)
    return date.replace(day=31) if date.month==12 else \
           (date.replace(month=date.month+1, day=1)-timedelta(days=1))


def get_week_start_dateid(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_week_start_dateid(date=20220629)
    20220627
    """
    date = parse_datetime(dt=date)
    week_start_date = date - timedelta(days=date.weekday())
    return normalize_date_to_dateid(date=week_start_date)


def get_month_start_dateid(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_month_start_dateid(date=20220629)
    20220601
    """
    date = parse_datetime(dt=date)
    return normalize_date_to_dateid(date=date.replace(day=1))


def get_year_start_dateid(date=None):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_year_start_dateid(date=20220629)
    20220101
    """
    if date is None:
        date = curr_dateid()

    date = parse_datetime(dt=date)
    return normalize_date_to_dateid(date=date.replace(month=1, day=1))


def get_ttm_start_dateid(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_ttm_start_dateid(date=20220629)
    20210629
    >>> dtu.get_ttm_start_dateid(date=20200229)
    20190228
    """
    date = parse_datetime(dt=date)
    try:
        ttm_start_date = date.replace(year=date.year-1)
    except:
        ttm_start_date = date.replace(year=date.year-1, day=date.day-1)

    return normalize_date_to_dateid(date=ttm_start_date)


def get_quarter_start_dateid(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_quarter_start_dateid(date=20220630)
    20220401
    >>> dtu.get_quarter_start_dateid(date=20220715)
    20220701
    """
    date = parse_datetime(dt=date)
    quarter_start_date = datetime(date.year, 3 * ((date.month - 1) // 3) + 1, 1)
    return normalize_date_to_dateid(date=quarter_start_date)


EXCHANGE_SESSIONS_CFG = None
def get_exchange_sessions_cfg():
    global EXCHANGE_SESSIONS_CFG
    if EXCHANGE_SESSIONS_CFG is None:
        exchange_sessions_cfg = f'''MIC,Region,Timezone,OpenTimeLocal,CloseTimeLocal
XASX,AP,Australia/Sydney,10:00:00,16:00:00
XSES,AP,Asia/Singapore,09:00:00,17:00:00
XHEL,EU,Europe/Helsinki,10:00:00,18:25:00
XLIS,EU,Europe/Lisbon,08:00:00,16:30:00
XNYS,US,America/New_York,09:30:00,16:00:00
        '''

        EXCHANGE_SESSIONS_CFG = pd.read_csv(StringIO(exchange_sessions_cfg), sep=',')

    return EXCHANGE_SESSIONS_CFG



def get_exchange_sessions(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_exchange_sessions(date=20220425)
        MIC Region          Timezone OpenTimeLocal CloseTimeLocal          OpenDateTimeLocal         CloseDateTimeLocal           OpenDateTimeUTC          CloseDateTimeUTC
    0  XASX     AP  Australia/Sydney      10:00:00       16:00:00  2022-04-25 10:00:00+10:00  2022-04-25 16:00:00+10:00 2022-04-25 00:00:00+00:00 2022-04-25 06:00:00+00:00
    1  XSES     AP    Asia/Singapore      09:00:00       17:00:00  2022-04-25 09:00:00+08:00  2022-04-25 17:00:00+08:00 2022-04-25 01:00:00+00:00 2022-04-25 09:00:00+00:00
    2  XHEL     EU   Europe/Helsinki      10:00:00       18:25:00  2022-04-25 10:00:00+03:00  2022-04-25 18:25:00+03:00 2022-04-25 07:00:00+00:00 2022-04-25 15:25:00+00:00
    3  XLIS     EU     Europe/Lisbon      08:00:00       16:30:00  2022-04-25 08:00:00+01:00  2022-04-25 16:30:00+01:00 2022-04-25 07:00:00+00:00 2022-04-25 15:30:00+00:00
    4  XNYS     US  America/New_York      09:30:00       16:00:00  2022-04-25 09:30:00-04:00  2022-04-25 16:00:00-04:00 2022-04-25 13:30:00+00:00 2022-04-25 20:00:00+00:00
    >>> dtu.get_exchange_sessions(date=20230422)
        MIC Region          Timezone OpenTimeLocal CloseTimeLocal          OpenDateTimeLocal         CloseDateTimeLocal           OpenDateTimeUTC          CloseDateTimeUTC
    0  XASX     AP  Australia/Sydney      10:00:00       16:00:00  2023-04-24 10:00:00+10:00  2023-04-24 16:00:00+10:00 2023-04-24 00:00:00+00:00 2023-04-24 06:00:00+00:00
    1  XSES     AP    Asia/Singapore      09:00:00       17:00:00  2023-04-24 09:00:00+08:00  2023-04-24 17:00:00+08:00 2023-04-24 01:00:00+00:00 2023-04-24 09:00:00+00:00
    2  XHEL     EU   Europe/Helsinki      10:00:00       18:25:00  2023-04-24 10:00:00+03:00  2023-04-24 18:25:00+03:00 2023-04-24 07:00:00+00:00 2023-04-24 15:25:00+00:00
    3  XLIS     EU     Europe/Lisbon      08:00:00       16:30:00  2023-04-24 08:00:00+01:00  2023-04-24 16:30:00+01:00 2023-04-24 07:00:00+00:00 2023-04-24 15:30:00+00:00
    4  XNYS     US  America/New_York      09:30:00       16:00:00  2023-04-24 09:30:00-04:00  2023-04-24 16:00:00-04:00 2023-04-24 13:30:00+00:00 2023-04-24 20:00:00+00:00
    >>> dtu.get_exchange_sessions(date=20230101)
        MIC Region          Timezone OpenTimeLocal CloseTimeLocal          OpenDateTimeLocal         CloseDateTimeLocal           OpenDateTimeUTC          CloseDateTimeUTC
    0  XASX     AP  Australia/Sydney      10:00:00       16:00:00  2024-01-02 10:00:00+11:00  2024-01-02 16:00:00+11:00 2024-01-01 23:00:00+00:00 2024-01-02 05:00:00+00:00
    1  XSES     AP    Asia/Singapore      09:00:00       17:00:00  2024-01-02 09:00:00+08:00  2024-01-02 17:00:00+08:00 2024-01-02 01:00:00+00:00 2024-01-02 09:00:00+00:00
    2  XHEL     EU   Europe/Helsinki      10:00:00       18:25:00  2024-01-02 10:00:00+02:00  2024-01-02 18:25:00+02:00 2024-01-02 08:00:00+00:00 2024-01-02 16:25:00+00:00
    3  XLIS     EU     Europe/Lisbon      08:00:00       16:30:00  2024-01-02 08:00:00+00:00  2024-01-02 16:30:00+00:00 2024-01-02 08:00:00+00:00 2024-01-02 16:30:00+00:00
    4  XNYS     US  America/New_York      09:30:00       16:00:00  2024-01-02 09:30:00-05:00  2024-01-02 16:00:00-05:00 2024-01-02 14:30:00+00:00 2024-01-02 21:00:00+00:00
    """

    exchange_sessions = get_exchange_sessions_cfg().copy()

    def infer_dt_local(row, time_col):
        dateid = normalize_date_to_dateid(date=date)
        dateid = dateid if is_weekday(date=date) and str(dateid)[-4:]!='0101' else next_biz_dateid(dateid=dateid)
        dt_str = f"{dateid} {row[time_col]}"
        return parse_datetime(dt_str, timezone=row['Timezone'])

    exchange_sessions['OpenDateTimeLocal'] = exchange_sessions.apply(lambda x : infer_dt_local(x, 'OpenTimeLocal'), axis=1)
    exchange_sessions['CloseDateTimeLocal'] = exchange_sessions.apply(lambda x : infer_dt_local(x, 'CloseTimeLocal'), axis=1)

    exchange_sessions['OpenDateTimeUTC'] = exchange_sessions['OpenDateTimeLocal'].apply(lambda x : x.astimezone(timezone.utc))
    exchange_sessions['CloseDateTimeUTC'] = exchange_sessions['CloseDateTimeLocal'].apply(lambda x: x.astimezone(timezone.utc))

    return exchange_sessions


def get_region_sessions(date):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.get_region_sessions(date=20230425)
                    StartDateTimeUTC            EndDateTimeUTC
    Region
    AP     2023-04-25 00:00:00+00:00 2023-04-25 09:00:00+00:00
    EU     2023-04-25 07:00:00+00:00 2023-04-25 15:30:00+00:00
    US     2023-04-25 13:30:00+00:00 2023-04-25 20:00:00+00:00
    WW     2023-04-25 00:00:00+00:00 2023-04-25 20:00:00+00:00
    >>> dtu.get_region_sessions(date=20230402)
                    StartDateTimeUTC            EndDateTimeUTC
    Region
    AP     2023-04-03 00:00:00+00:00 2023-04-03 09:00:00+00:00
    EU     2023-04-03 07:00:00+00:00 2023-04-03 15:30:00+00:00
    US     2023-04-03 13:30:00+00:00 2023-04-03 20:00:00+00:00
    WW     2023-04-03 00:00:00+00:00 2023-04-03 20:00:00+00:00
    >>> dtu.get_region_sessions(date=20240101)
                    StartDateTimeUTC            EndDateTimeUTC
    Region
    AP     2024-01-01 23:00:00+00:00 2024-01-02 09:00:00+00:00
    EU     2024-01-02 08:00:00+00:00 2024-01-02 16:30:00+00:00
    US     2024-01-02 14:30:00+00:00 2024-01-02 21:00:00+00:00
    WW     2024-01-01 23:00:00+00:00 2024-01-02 21:00:00+00:00
    """
    exchange_sessions = get_exchange_sessions(date=date)
    region_sessions = exchange_sessions.groupby('Region').apply(
        lambda x : pd.DataFrame.from_dict({'OpenDateTimeUTC':x['OpenDateTimeUTC'].min(),
                                           'CloseDateTimeUTC':x['CloseDateTimeUTC'].max()},
                                          orient='index')
    )
    region_sessions = region_sessions[0].unstack()
    region_sessions.loc['WW'] = [region_sessions['OpenDateTimeUTC'].min(), region_sessions['CloseDateTimeUTC'].max()]

    region_sessions.rename(columns={'OpenDateTimeUTC':'StartDateTimeUTC',
                                    'CloseDateTimeUTC':'EndDateTimeUTC'},
                           inplace=True)

    return region_sessions


def infer_region_cutoff_dts(dateid=None, now=None,
                            region='WW',
                            ext_minutes=None):
    """
    >>> import qtc.utils.datetime_utils as dtu
    >>> dtu.infer_region_cutoff_dts(dateid=20240101)
    (Timestamp('2024-01-01 23:00:00+0000', tz='UTC'),
     Timestamp('2024-01-02 21:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(dateid=20230422)
    (Timestamp('2023-04-24 00:00:00+0000', tz='UTC'),
     Timestamp('2023-04-24 20:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(dateid=20230425)
    (Timestamp('2023-04-25 00:00:00+0000', tz='UTC'),
     Timestamp('2023-04-25 20:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2023-04-24 10:00:00+00:00', ext_minutes=15)
    (Timestamp('2023-04-23 23:45:00+0000', tz='UTC'),
     Timestamp('2023-04-24 20:15:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2023-04-24 21:00:00+00:00')
    (Timestamp('2023-04-25 00:00:00+0000', tz='UTC'),
     Timestamp('2023-04-25 20:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2023-04-25 01:00:00+00:00')
    (Timestamp('2023-04-25 00:00:00+0000', tz='UTC'),
     Timestamp('2023-04-25 20:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2024-01-01 22:00:00+00:00')
    (Timestamp('2024-01-01 23:00:00+0000', tz='UTC'),
     Timestamp('2024-01-02 21:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2024-01-01 23:30:00+00:00')
    (Timestamp('2024-01-01 23:00:00+0000', tz='UTC'),
     Timestamp('2024-01-02 21:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2024-01-02 10:00:00+00:00')
    (Timestamp('2024-01-01 23:00:00+0000', tz='UTC'),
     Timestamp('2024-01-02 21:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2024-01-02 22:00:00+00:00')
    (Timestamp('2024-01-02 23:00:00+0000', tz='UTC'),
     Timestamp('2024-01-03 21:00:00+0000', tz='UTC'))
    >>> dtu.infer_region_cutoff_dts(now='2024-01-03 10:00:00+00:00')
    (Timestamp('2024-01-02 23:00:00+0000', tz='UTC'),
     Timestamp('2024-01-03 21:00:00+0000', tz='UTC'))
    """
    if dateid is None:
        if now is None:
            now = datetime.now(tz=pytz.timezone('UTC'))
        if not isinstance(now, datetime):
            now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S%z')
        now = now.astimezone(pytz.timezone('UTC'))

        dateid = normalize_date_to_dateid(date=now)
        start_dt, end_dt = infer_region_cutoff_dts(dateid=dateid,
                                                   region=region,
                                                   ext_minutes=ext_minutes)
        # print(f'now={now}, end_dt={end_dt}, dateid={dateid}, next_biz_dateid={next_biz_dateid(dateid=dateid)}')
        if now>end_dt:
            start_dt, end_dt = infer_region_cutoff_dts(dateid=next_biz_dateid(dateid=dateid),
                                                       region=region,
                                                       ext_minutes=ext_minutes)
    else:
        region_sessions = get_region_sessions(date=dateid)

        tz_name = 'UTC'
        if ext_minutes is None:
            ext_minutes = 0

        if region is None:
            region = 'WW'
        start_dt = region_sessions.loc[region, 'StartDateTimeUTC'].to_pydatetime() - timedelta(minutes=ext_minutes)
        end_dt = region_sessions.loc[region, 'EndDateTimeUTC'].to_pydatetime() + timedelta(minutes=ext_minutes)

        ## Backward compatibility
        try:
            end_dt = pytz.timezone(tz_name).localize(end_dt)
            start_dt = pytz.timezone(tz_name).localize(start_dt)
        except:
            pass

    start_dt = pd.Timestamp(start_dt)
    end_dt = pd.Timestamp(end_dt)
    return start_dt, end_dt


# TRADING_SESSIONS = None
# def get_trading_sessions():
#     global TRADING_SESSIONS
#     if TRADING_SESSIONS is None:
#
#         # REGION_MICS = pd.read_csv(StringIO(f'Region,FirstMIC,LastMIC\nAP,XASX,XSES\nEU,XHEL,XLIS\nUS,XNYS,XNYS'),
#         #                           index_col='Region')
#         cfg = f'''
# Region,FirstExMIC,FirstExTZ,FirstExOpenTimeLocal,FirstExCloseTimeLocal,LastExMIC,LastExTZ,LastExOpenTimeLocal,LastExCloseTimeLocal
# AP,XASX,Australia/Sydney,10:00:00,16:00:00,XSES,Asia/Singapore,09:00:00,17:00:00
# EU,XHEL,Europe/Helsinki,10:00:00,18:25:00,XLIS,Europe/Lisbon,08:00:00,16:30:00
# US,XNYS,America/New_York,09:30:00,16:00:00,XNYS,America/New_York,09:30:00,16:00:00
# WW,XASX,Australia/Sydney,10:00:00,16:00:00,XNYS,America/New_York,09:30:00,16:00:00
#         '''
#         TRADING_SESSIONS = pd.read_csv(StringIO(cfg), index_col='Region')
#
#     return TRADING_SESSIONS


# def get_region_start_end_dt(dateid=None, region=None,
#                             now=None,
#                             ext_minutes=0):
#     """
#     >>> import qtc.utils.datetime_utils as dtu
#     >>> dtu.get_region_start_end_dt(dateid=20230417)
#     (Timestamp('2023-04-17 00:00:00+0000', tz='UTC'),
#      Timestamp('2023-04-17 20:00:00+0000', tz='UTC'))
#     >>> dtu.get_region_start_end_dt(dateid=20230416)
#     (Timestamp('2023-04-17 00:00:00+0000', tz='UTC'),
#      Timestamp('2023-04-17 20:00:00+0000', tz='UTC'))
#     >>> dtu.get_region_start_end_dt(dateid=20230103)
#     (Timestamp('2023-01-02 23:00:00+0000', tz='UTC'),
#      Timestamp('2023-01-03 21:00:00+0000', tz='UTC'))
#     >>> dtu.get_region_start_end_dt(now='2023-04-17 16:30:00-0400', ext_minutes=15)
#     (Timestamp('2023-04-17 23:45:00+0000', tz='UTC'),
#      Timestamp('2023-04-18 20:15:00+0000', tz='UTC'))
#     >>> dtu.get_region_start_end_dt(dateid=20230425)
#     (Timestamp('2023-04-25 00:00:00+0000', tz='UTC'),
#      Timestamp('2023-04-25 20:00:00+0000', tz='UTC'))
#     """
#     region_mics = get_region_mics()
#     if region is None:
#         first_mic, _ = region_mics.loc['AP']
#         _, last_mic = region_mics.loc['US']
#     else:
#         first_mic, last_mic = region_mics.loc[region]
#
#     import pandas_market_calendars as mcal
#     fmic = mcal.get_calendar(first_mic.upper())
#     lmic = mcal.get_calendar(last_mic.upper())
#
#     if dateid is None:
#         if now is None:
#             now = datetime.now(tz=pytz.timezone('America/New_York'))
#         else:
#             if not isinstance(now, datetime):
#                 now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S%z')
#     else:
#         now = dateid_to_datetime(dateid=dateid, timezone='America/New_York')
#
#     start_dt = end_dt = None
#     while True:
#         dateid = normalize_date_to_dateid(date=now)
#         datestr = dateid_to_datestr(dateid=dateid, sep='-')
#
#         # try:
#         #     start_dt = fmic.schedule(start_date=datestr, end_date=datestr)['market_open'][0] - timedelta(minutes=ext_minutes)
#         #     end_dt = lmic.schedule(start_date=datestr, end_date=datestr)['market_close'][0] + timedelta(minutes=ext_minutes)
#         # except:
#         #     now = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
#         #     continue
#
#         fschedule = fmic.schedule(start_date=datestr, end_date=datestr)
#         if len(fschedule)>0:
#             start_dt = fschedule['market_open'][0] - timedelta(minutes=ext_minutes)
#
#         lschedule = lmic.schedule(start_date=datestr, end_date=datestr)
#         if len(lschedule)>0:
#             end_dt = lschedule['market_close'][0] + timedelta(minutes=ext_minutes)
#
#         if start_dt is None:
#             if end_dt is None:
#                 now = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
#                 continue
#         else:
#             if end_dt is None:
#                 end_dt = (start_dt.astimezone(pytz.timezone('America/New_York')) + timedelta(days=1)).replace(hour=16, minute=0, second=0) + timedelta(minutes=ext_minutes)
#
#         if now > end_dt:
#             now = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
#             continue
#
#         break
#
#     if start_dt is None:
#         start_dt = (end_dt.astimezone(pytz.timezone('Australia/Sydney')) - timedelta(days=1))
#         start_dt = start_dt.replace(hour=10, minute=0, second=0) - timedelta(minutes=ext_minutes)
#         start_dt = start_dt.astimezone(tz=pytz.timezone('UTC'))
#
#     return start_dt, end_dt

# def get_region_start_end_dt(dateid=None, region=None,
#                             now=None,
#                             ext_minutes=0):
#     if region is None:
#         region = 'WW'
#
#     session = get_trading_sessions().loc[region]
#
#     if now is None:
#         now = datetime.now(tz=pytz.timezone('America/New_York'))
#         end_dt = now.replace()
#
#     if dateid is None:
#         dateid = normalize_date_to_dateid(date=now)
#
#     start_dt = dateid_to_datetime(dateid=dateid, timezone=ftz).replace(hour=10, minute=0, second=0).astimezone(tz=pytz.timezone('UTC'))
#     end_dt = dateid_to_datetime(dateid=dateid, timezone=ltz).replace(hour=10, minute=0, second=0).astimezone(
#         tz=pytz.timezone('UTC'))

