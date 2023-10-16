import qtc.utils.misc_utils as mu
import qtc.utils.db_utils as dbu
import qtc.data.dal.common.sql_compiler as sqlc

def query_market(start_dateid=None, end_dateid=None, dateids=None,
                 security_codes=None,
                 cols=None,
                 database='CN-EQUITY-VENDOR',
                 **db_config):
    """
    >>> import qtc.data.dal.sec as dalsec
    >>> dalsec.query_market(dateids=20230519)
    """
    sql_and_clauses = list()
    if security_codes is not None:
        security_codes_db_str = mu.iterable_to_db_str(security_codes, raw_type='str')
        sql_and_clauses.append(f'"ts_code" IN {security_codes_db_str}')

    dateid_sql_and_clauses = sqlc.build_dateid_sql_and_clauses(
        start_dateid=start_dateid, end_dateid=end_dateid, dateids=dateids,
        quotes_on_colnames=True
    )
    dateid_sql_and_clauses = [s.replace('DateId','trade_date') for s in dateid_sql_and_clauses]
    sql_and_clauses.extend(dateid_sql_and_clauses)

    sql = f'''
        SELECT * FROM "tushare"."DailyMarketData"
        {dbu.compile_sql_where_clause(sql_and_clauses)}
    '''

    conn = dbu.get_os_env_conn(database=database,
                               **db_config)
    required_cols = ['trade_date','ts_code']
    market_data = dbu.sql2df(sql=sql, conn=conn,
                             required_cols=required_cols, cols=cols,
                             preprocess_cols=False,
                             quotes_on_colnames=True)
    return market_data
