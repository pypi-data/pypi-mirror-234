from functools import lru_cache
import qtc.utils.db_utils as dbu
import qtc.utils.misc_utils as mu


@lru_cache
def query_calendar(exchanges=None,
                   is_open=True,
                   database='CN-EQUITY-VENDOR',
                   **db_config):
    """
    >>> import qtc.data.dal.calendar as dalcal
    >>> dalcal.query_calendar().head()
      exchange  cal_date  is_open             UpdateDateTime
    0      SSE  20231231    False 2023-05-15 13:25:24.219822
    1      SSE  20231230    False 2023-05-15 13:25:24.219822
    2      SSE  20231229     True 2023-05-15 13:25:24.219822
    3      SSE  20231228     True 2023-05-15 13:25:24.219822
    4      SSE  20231227     True 2023-05-15 13:25:24.219822
    >>> dalcal.query_calendar(exchanges='SSE,SZSE').tail()
          exchange  cal_date  is_open             UpdateDateTime
    23931     SZSE  19910707    False 2023-05-15 13:25:24.219822
    23932     SZSE  19910706    False 2023-05-15 13:25:24.219822
    23933     SZSE  19910705     True 2023-05-15 13:25:24.219822
    23934     SZSE  19910704     True 2023-05-15 13:25:24.219822
    23935     SZSE  19910703     True 2023-05-15 13:25:24.219822
    """

    sql_and_clauses = list()
    if exchanges is not None:
        exchanges_db_str = mu.iterable_to_db_str(exchanges, raw_type='str')
        sql_and_clauses.append(f'"exchange" IN {exchanges_db_str}')
    if is_open is not None:
        sql_and_clauses.append(f'"is_open" IS {str(is_open).upper()}')

    sql = f'''
        SELECT * FROM "mktmeta"."Calendar"
        {dbu.compile_sql_where_clause(sql_and_clauses)}
    '''

    conn = dbu.get_os_env_conn(database=database,
                               **db_config)
    # print(conn)
    calendar = dbu.sql2df(sql=sql, conn=conn,
                          preprocess_cols=False,
                          quotes_on_colnames=True)
    return calendar
