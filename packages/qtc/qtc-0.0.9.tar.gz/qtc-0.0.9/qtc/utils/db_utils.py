import os
import re
import time
import getpass
import traceback
from functools import lru_cache
import pandas as pd
import sqlalchemy
from urllib.parse import quote
from typing import Optional, Dict
from qtc.consts.enums import DBType
import qtc.env_config as ecfg
import qtc.utils.misc_utils as mu
from qtc.ext.logging import set_logger
logger = set_logger()

import warnings
warnings.filterwarnings('ignore')


def _get_conn_mssql(host, port, user, password,
                    database=None):
    if port is None:
        port = 1433

    logger.debug(f'host={host}, port={port}, user={user}, password={password}, database={database}')
    import pymssql
    if os.name == 'nt':  # windows
        conn = pymssql.connect(user=user, password=password,
                               host=host, port=port)
    elif os.name == 'posix':  # linux
        if database:
            conn = pymssql.connect(user=user, password=password,
                                   host=host, port=port,
                                   database=database)
        else:
            conn = pymssql.connect(user=user, password=password,
                                   host=host, port=port)

    if conn:
        conn.autocommit(True)

    return conn


def _get_conn_redshift(host, port, user, password,
                       database=None):
    # if host.upper() == 'REDSHIFT':
    #     host = ecfg.get_env_config().get(prop='redshift.host')
    #     if port is None:
    #         port = ecfg.get_env_config().get(prop='redshift.port', default=5439)
    if port is None:
        port = ecfg.get_env_config().get(prop='redshift.port', default=5439)

    if database is None:
        database = 'bigdataprod'

    logger.debug(f'host={host}, port={port}, user={user}, password={password}, database={database}')
    import psycopg2
    conn = psycopg2.connect(user=user, password=password,
                            host=host, port=port,
                            database=database)
    if conn:
        conn.set_session(autocommit=True)

    return conn


def _get_engine(db_type,
                host, port, user, password,
                database=None):
    if isinstance(db_type, str):
        db_type = DBType.retrieve(value=db_type)

    if db_type==DBType.POSTGRES:
        conn_string = f'postgresql://{user}:{quote(password)}@{host}:{port}'
    else:
        raise Exception(f'db_type={db_type} is not supported in [POSTGRES] !')

    if database is not None:
        conn_string = f'{conn_string}/{database}'

    # print(conn_string)
    engine = sqlalchemy.create_engine(conn_string)
    return engine


def _get_conn_postgres(host, port, user, password,
                       database=None):
    engine = _get_engine(db_type=DBType.POSTGRES,
                         host=host, port=port, user=user, password=password,
                         database=database)
    conn = engine.connect()
    return conn


# def _get_conn_mysql(host, port, user, password,
#                     database=None):
#     # engine = _get_engine(db_type=DBType.MYSQL,
#     #                      host=host, port=port, user=user, password=password,
#     #                      database=database)
#     # conn = engine.connect()
#     import pymysql
#     conn = pymysql.connect(host=host, port=int(port), user=user, passwd=password, db=database)
#
#     return conn


def _init_conn(host, port=None,
               user=None, password=None,
               database=None,
               db_type=None):

    conn = None
    if db_type is None:
        try:
            conn = _get_conn_postgres(host=host, port=port, user=user, password=password, database=database)
        except:
            try:
                conn = _get_conn_mssql(host=host, port=port, user=user, password=password, database=database)
            except:
                try:
                    conn = _get_conn_mysql(host=host, port=port, user=user, password=password, database=database)
                except:
                    try:
                        conn = _get_conn_redshift(host=host, port=port, user=user, password=password, database=database)
                    except:
                        logger.warn(f'Unable to create connection by db_type=[MSSQL|MYSQL|REDSHIFT|POSTGRES] with '
                                    f'host={host}, port={port}, user={user}, password={password}, database={database} !')
                        return None
        return conn

    if isinstance(db_type, str):
        db_type = DBType.retrieve(value=db_type)

    if user is None:
        user = getpass.getuser()

    if db_type==DBType.MSSQL:
        conn = _get_conn_mssql(host=host, port=port, user=user, password=password, database=database)
    # elif db_type==DBType.MYSQL:
    #     conn = _get_conn_mysql(host=host, port=port, user=user, password=password, database=database)
    elif db_type==DBType.REDSHIFT:
        conn = _get_conn_redshift(host=host, port=port, user=user, password=password, database=database)
    elif db_type==DBType.POSTGRES:
        conn = _get_conn_postgres(host=host, port=port, user=user, password=password, database=database)
    else:
        logger.error(f'db_type={db_type} is not supported in [MSSQL | REDSHIFT | POSTGRES] !')

    return conn


def _get_conn_with_retry(host, port=None,
                         user=None, password=None,
                         database=None,
                         db_type=None,
                         max_retry=0, retry_interval=60):
    conn = None
    n_try = 0
    while conn is None and n_try<=max_retry:
        if n_try != 0:
            logger.warn(f'Sleeping for {retry_interval} seconds before {n_try} retry ...')
            time.sleep(retry_interval)

        try:
            conn = _init_conn(host=host, port=port,
                              user=user, password=password,
                              database=database,
                              db_type=db_type)
        except:
            pass

        n_try += 1

    if conn is None and max_retry>0:
        logger.error(f'Failed to init conn after {max_retry} retries !')

    return conn


def _infer_db_type_name(db_code):
    """
    >>> import qtc.utils.db_utils as dbu
    >>> dbu._infer_db_type_name(db_code='DW-DB')
    (<DBType.MSSQL: 'MSSQL'>, 'DW-DB')
    >>> dbu._infer_db_type_name(db_code='DW-DB.host')
    (<DBType.MSSQL: 'MSSQL'>, 'DW-DB')
    >>> dbu._infer_db_type_name(db_code='redshift.host')
    (<DBType.REDSHIFT: 'REDSHIFT'>, 'redshift')
    >>> dbu._infer_db_type_name(db_code='redshift.bamfunds.net')
    (<DBType.REDSHIFT: 'REDSHIFT'>, 'redshift.bamfunds.net')
    """
    db_name = db_code.replace('.host', '') if '.host' in db_code else db_code

    mssql_dbs = ecfg.get_env_config().get('mssql_dbs', '')
    mssql_dbs = set(mu.iterable_to_tuple(mssql_dbs, raw_type='str'))

    mysql_dbs = ecfg.get_env_config().get('mysql_dbs', 'GMBP-ADS,GMBP-RDS')
    mysql_dbs = set(mu.iterable_to_tuple(mysql_dbs, raw_type='str'))

    postgres_dbs = ecfg.get_env_config().get('postgres_dbs', '')
    postgres_dbs = set(mu.iterable_to_tuple(postgres_dbs, raw_type='str'))

    if db_name.upper() in mysql_dbs or db_name.split('.')[0].upper() in mysql_dbs:
        db_type = DBType.MYSQL
    elif db_name.upper() in mssql_dbs or db_name.split('.')[0].upper() in mssql_dbs:
        db_type = DBType.MSSQL
    elif db_name.upper() in postgres_dbs or db_name.split('.')[0].upper() in postgres_dbs:
        db_type = DBType.POSTGRES
    elif db_name.upper() in ('REDSHIFT') or 'redshift' in db_code:
        db_type = DBType.REDSHIFT
    else:
        db_type = None

    return db_type, db_name


def _get_db_config(db_code, **db_config):
    db_type, db_name = _infer_db_type_name(db_code=db_code)
    host, port, user, password, database = infer_db_config(db_code=db_code, **db_config)

    return host, port, user, password, database, db_type, db_name


def get_conn(db_code, **db_config):
    host, port, user, password, database, db_type, db_name = _get_db_config(db_code=db_code, **db_config)

    return _get_conn_with_retry(host=host, port=port,
                                user=user, password=password,
                                database=database,
                                db_type=db_type,
                                max_retry=0, retry_interval=60)


def execute_sql(sql,
                host=None, conn=None,
                log_sql=False):
    if conn is None:
        conn = get_conn(db_code=host)

    if conn is None:
        logger.error(f'Failed to get connection to run sql={sql} against host={host} !')

    if log_sql:
        logger.debug(f"Connection: {conn}")
        logger.debug(f"SQL Query:\n{sql}")

    if os.path.isfile(sql):
        with open(sql, 'r') as fh:
            sql = fh.read()

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except Exception as e:
        logger.error(f"Exception caught when executing:\n{sql}")
        traceback.print_exc()
    finally:
        conn.close()

    return


def read_sql(sql,
             host=None, database=None, conn=None,
             log_sql=False, params=None):
    """Wraps pandas read_sql function. For raw SQL queries without columns selections, this function is perferred.

    >>> import qtc.utils.db_utils as dbu
    >>> dbu.read_sql(sql='SELECT * FROM "mktmeta"."Calendar"',
                     host='DB', database='CN-EQUITY-VENDOR').head()
      exchange  cal_date  is_open             UpdateDateTime
    0      SSE  20231231    False 2023-10-06 09:05:13.248403
    1      SSE  20231230    False 2023-10-06 09:05:13.248403
    2      SSE  20231229     True 2023-10-06 09:05:13.248403
    3      SSE  20231228     True 2023-10-06 09:05:13.248403
    4      SSE  20231227     True 2023-10-06 09:05:13.248403
    """

    if conn is None:
        conn = get_conn(db_code=host, database=database)

    if conn is None:
        logger.error(f'Failed to get connection to run sql={sql} against host={host} !')

    if log_sql:
        logger.debug(f"Connection: {conn}")
        logger.debug(f"SQL Query:\n{sql}")

    df = None
    try:
        df = pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()

    return df


def _query_headers(sql,
                   host=None, conn=None):
    """Helper function to get headers from DB table contained in the SQL query.
    >>> import qtc.utils.db_utils as dbu
    >>> dbu._query_headers(sql="SELECT * FROM ANTH_REFERENCE.trd.RESTRICTIONS (NOLOCK) " \
                               "WHERE DATA_DATE='2022-05-04'",
                           host='ANTHSYSEQ-DB')
    Index(['DATA_DATE', 'CODE', 'TICKER', 'COUNTRY', 'TYPE', 'MODE', 'SOURCE', 'REASON', 'ENTRY_TIME'], dtype='object')
    """

    try:
        select_top_1_sql = re.sub('SELECT[ ]+.*\s*FROM', 'SELECT TOP 1 * FROM', sql, flags=re.IGNORECASE)
        ret = read_sql(sql=select_top_1_sql, host=host, conn=conn).columns
    except:
        select_top_1_sql = re.sub('SELECT[ ]+.*\s*FROM', 'SELECT * FROM', sql, flags=re.IGNORECASE) + ' FETCH FIRST ROW ONLY'
        ret = read_sql(sql=select_top_1_sql, host=host, conn=conn).columns

    return ret


def _process_cols(available_cols, required_cols=None, expected_cols=None,
                  raise_exception_on_not_found_required_cols=False,
                  sql=None):
    """Infers the final columns based on all "available_cols", "required_cols"(usually key columns in the DB table)
    and user "expected_cols", which could overlap with "required_cols".
    If "required_cols" is not None, then the returned cols will have "required_cols" first and then other columns if more columns should be returned.
    If "expected_cols" is None, then return all "available_cols". Otherwise, return "required_cols"+"expected_cols".

    :param available_cols: All available columns. Please note that it cannot be None.
    :type available_cols: str | int | Iterable. See :func:`qtc.utils.misc.iterable_to_tuple`
    :param required_cols: Required columns. If not found in the available columns, exception handling will depend on 'raise_exception_on_not_found_required_cols'.
    :type required_cols: str | int | Iterable. See :func:`qtc.utils.misc.iterable_to_tuple`
    :param expected_cols: User expected columns.
    :type expected_cols: str | int | Iterable. See :func:`qtc.utils.misc.iterable_to_tuple`
    :param raise_exception_on_not_found_required_cols: If True, throw exception if there are some required columns which cannot be found in available columns.
    :type raise_exception_on_not_found_required_cols: bool
    :return: list - Return columns.

    >>> import qtc.utils.db_utils as dbu
    >>> dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return', required_cols='SecurityId', expected_cols='NMV,Return')
    ['SecurityId', 'NMV', 'Return']
    >>> dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return', required_cols='SecurityId,NMV', expected_cols='NMV,Return,SecurityId')
    ['SecurityId', 'NMV', 'Return']
    >>> dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return', required_cols='SecurityId,NMV,BbergCode')
    ['SecurityId', 'NMV', 'BbergCode', 'AxiomaId', 'Return']
    >>> dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return', required_cols='SecurityId,DisplayCode')
    [2019-12-06 17:24:20,822: bamrisk.utils.db_utils - process_cols()] ERROR - Failed to find these required columns: ['DisplayCode'] in available columns: ['SecurityId', 'AxiomaId', 'BbergCode', 'NMV', 'Return']
    ['SecurityId', 'AxiomaId', 'BbergCode', 'NMV', 'Return']
    >>> dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return', expected_cols='SecurityId,NMV')
    ['SecurityId', 'NMV']
    """
    available_cols = list(mu.iterable_to_tuple(available_cols, raw_type='str'))
    available_cols_upper = [col.upper() for col in available_cols]

    if required_cols is None:
        required_cols = expected_cols

    sql = '' if sql is None else f"\n{sql}"

    ret_cols = list()
    if required_cols is not None:
        # Check if all required_cols are in available_cols
        required_cols = list(mu.iterable_to_tuple(required_cols, raw_type='str'))
        # not_found_cols = [col for col in required_cols if col not in available_cols]
        not_found_cols = [col for col in required_cols if col.upper() not in available_cols_upper]
        if len(not_found_cols) > 0:
            if raise_exception_on_not_found_required_cols:
                raise Exception(f"Failed to find these required columns: {not_found_cols} in available columns: {available_cols}{sql}")
            else:
                logger.error(f"Failed to find these required columns: {not_found_cols} in available columns: {available_cols}{sql}")
                required_cols = [col for col in required_cols if col.upper() in available_cols_upper]

        ret_cols = required_cols

    ret_cols_upper = [col.upper() for col in ret_cols]
    if expected_cols is None:
        for col in available_cols:
            if col.upper() not in ret_cols_upper:
                ret_cols.append(col)

        return ret_cols

    ret_cols_upper = [col.upper() for col in ret_cols]
    expected_cols = list(mu.iterable_to_tuple(expected_cols, raw_type='str'))
    not_found_cols = list()
    for col in expected_cols:
        if col.upper() not in available_cols_upper:
            not_found_cols.append(col)
        else:
            if col.upper() not in ret_cols_upper:
                ret_cols.append(col)

    if len(not_found_cols)>0:
        logger.warn(f"Failed to find these expected columns: {not_found_cols} in available columns: {available_cols}\n{sql}")

    return ret_cols


def _modify_sql(sql, required_cols=None, expected_cols=None,
                available_cols=None,
                host=None, conn=None,
                quotes_on_colnames=False):
    """A helper function to infer the minimal set of columns to query and modify the original query accordingly.

    .. note::
        #. Andrew Hu's philosophy for DB access layer is that the SQL queries should be as "atomic" as possible. So here the "sql" is simple query which usually only queries one DB table.
        #. 'available_cols', 'required_cols', 'expected_cols' are used in :func:`bamrisk_common.utils.db_utils._process_cols` to infer the minimal set of columns.

    :param sql: The SQL query statement.
    :param available_cols: All available columns. If None, then :func:`bamrisk.utils.db_utils.query_table_cols` is called to get the table columns, where 'db_prefix' matters.
    :type available_cols: str | int | Iterable. See :func:`bamrisk.utils.misc.iterable_to_tuple`
    :param required_cols: Required columns. If not found in the available columns, exception handling will depend on 'raise_exception_on_not_found_required_cols'.
    :type required_cols: str | int | Iterable. See :func:`bamrisk.utils.misc.iterable_to_tuple`
    :param expected_cols: User expected columns.
    :type expected_cols: str | int | Iterable. See :func:`bamrisk.utils.misc.iterable_to_tuple`
    :return: str - Modified query with the minimal set of columns in "SELECT".

    >>> import qtc.utils.db_utils as dbu
    >>> modified_sql, cols = dbu._modify_sql(sql='SELECT * FROM BamCorelite.sm.Security WITH (NOLOCK)',
                                             host='DW-DB',
                                             required_cols='SecurityId,Axioma',
                                             expected_cols='SecurityId,Axioma,DisplayCode')
    >>> modified_sql
    'SELECT SecurityId,Axioma,DisplayCode FROM BamCorelite.sm.Security WITH (NOLOCK)'
    >>> cols
    ['SecurityId', 'Axioma', 'DisplayCode']
    """
    if available_cols is None:
        available_cols = _query_headers(sql=sql, host=host, conn=conn)

    cols = _process_cols(available_cols=available_cols, required_cols=required_cols, expected_cols=expected_cols,
                         sql=sql)

    replace = f'''"{'","'.join(cols)}"''' if quotes_on_colnames else ','.join(cols)
    modified_sql = re.sub('SELECT[ ]+.*\s*FROM', f"SELECT {replace} FROM", sql, flags=re.IGNORECASE)

    return modified_sql, cols


def compile_sql_where_clause(sql_and_clauses=None):
    """
    >>> import qtc.utils.db_utils as dbu
    >>> dbu.compile_sql_where_clause()
    ''
    >>> dbu.compile_sql_where_clause("CountryCode IN ('US')")
    "WHERE CountryCode IN ('US')"
    >>> dbu.compile_sql_where_clause(['SecurityId IN (407,409)', 'FactorModelId=60'])
    'WHERE SecurityId IN (407,409)\n\t\tAND FactorModelId=60'
    >>> dbu.compile_sql_where_clause("EffectiveStartDate<='2021-09-23'||EffectiveEndDate>='2020-09-23'")
    "WHERE EffectiveStartDate<='2021-09-23'\n\t\tAND EffectiveEndDate>='2020-09-23'"
    >>> dbu.compile_sql_where_clause(['SecurityId IN (407,409)', 'FactorModelId=60', ''])
    'WHERE SecurityId IN (407,409)\n\t\tAND FactorModelId=60'
    >>> dbu.compile_sql_where_clause([])

    """
    if sql_and_clauses is None or not sql_and_clauses:
        return ''

    sql_and_clauses = [sql_and_clause
                       for sql_and_clause in mu.iterable_to_tuple(sql_and_clauses, raw_type='str', sep='||')
                       if sql_and_clause is not None and sql_and_clause.strip()!='']
    sep = '\n\t\tAND '
    return f'WHERE {sep.join(sql_and_clauses)}' if sql_and_clauses else ''


def sql2df(sql, host=None, conn=None,
           required_cols=None, cols=None,
           preprocess_cols=True,
           log_df_head=False,
           quotes_on_colnames=False):
    """Queries DB server and return results in DataFrame.

    .. note::
        #. It is OK that columns defined in 'cols' are in 'required_cols'. A "union" of these two sets of columns will be returned.
        #. The orders of the columns are the same as in 'required_cols' and then the same as in 'cols'.
        #. If 'cols' is None, all columns will be returned.

    :param sql: SQL query statement.
    :type sql: str
    :param required_cols: Required columns to be in the results. If not found in the results, ERROR will be logged.
    :type required_cols: str | int | Iterable. See :func:`bamrisk.utils.misc.iterable_to_tuple`
    :param cols: Additional columns to keep in the results. If not found in the results, WARNING will be logged.
    :type cols: str | int | Iterable. See :func:`bamrisk.utils.misc.iterable_to_tuple`
    :return: DataFrame - The query results.

    >>> import qtc.utils.db_utils as dbu
    >>> dbu.sql2df(sql="SELECT * FROM ANTH_REFERENCE.ref.SECURITIES_MASTER_ARIES (NOLOCK) " \
                       "WHERE TICKER IN ('TSLA','GOOG') AND DATA_DATE='2022-05-04'",
                   host='ANTHSYSEQ-DB',
                   cols='DATA_DATE,CODE,SID,TICKER,EXCHANGE,BBG_FIGI,BBG_CFIGI')
        DATA_DATE      CODE           SID TICKER EXCHANGE      BBG_FIGI     BBG_CFIGI
    0  2022-05-04  10963872  ARS5c0d0abd8   TSLA      NAS  BBG000N9MNX3  BBG000N9MNX3
    1  2022-05-04  11131355  ARSbb22a4d90   GOOG      NAS  BBG009S3NB30  BBG009S3NB30
    2  2022-05-04  41228590  ARSefe51e330   GOOG      NLB  BBG0123139Y8  BBG012313950
    3  2022-05-04  41228591  ARS091d9b002   TSLA      NLB  BBG012313HF1  BBG012313GN4
    4  2022-05-04  62539930  ARS113f8d1a5   GOOG      SGO  BBG00YJL3ZW2  BBG00YJL3ZV3
    >>> dbu.sql2df(sql="SELECT * FROM ANTH_REFERENCE.ref.SECURITIES_MASTER_ARIES (NOLOCK) " \
                       "WHERE DATA_DATE='2022-05-04'",
                   host='ANTHSYSEQ-DB',
                   required_cols='DATA_DATE,CODE').head()
        DATA_DATE  CODE           SID   SID_MKTDATA     ISSUER_ID TICKER  PRI_RIC CONSOL_RIC MIC_CODE EXCHANGE COUNTRY CURRENCY SECTYPE SEC_SUBTYPE       SEC_DESC  PRIM_LIST_FLAG  COMPOSITE_FLAG COUNTRY_ORIGIN COUNTRY_EXPOSURE COUNTRY_INCORPORATION REGION    SEDOL      CUSIP          ISIN        CIK  CIQ_TRADINGITEMID  CIQ_COMPANYID   GVKEY IID BBG_TICKER_EXCH      BBG_FIGI     BBG_CFIGI    QAI_ID QAI_REGION  QAI_SEC_CODE  DS_INFO_CODE  DS_EXCH_INT_CODE FSYM_REGIONAL_ID FSYM_SECURITY_ID FSYM_ENTITY_ID  AXIOMA_ID  BAM_SECURITY_ID BAM_GENEVA_ID  BAM_MARKIT IBES_EST_PERM_ID IBES_TICKER IDC_CODE  WSPIT_SEC_CODE RIC_ARIES EXCHANGE_ARIES          ENTRY_TIME
    0  2022-05-04   779  ARS16ae50919  ARS16ae50919  ARC2b35627d7   AAON  AAON.OQ     AAON.O     XNGS      NAS      US      USD      EQ          cs    COM USD.001           False            True             US               US                    US   namr  2268130  000360206  US0003602069   824142.0          2585893.0       320500.0  021542  01         AAON US  BBG000C2LZP3  BBG000C2LZP3      AAON          U           779         52508               135         NWCBDX-R         HSDCT7-S       000ZGQ-E  6HS7Y1UZ3           2652.0             0     36279.0      30064826811        AAON  U-43029         30428.0    AAON.O            NAS 2022-05-04 04:59:57
    1  2022-05-04   780  ARS99baa08ba  ARS99baa08ba  ARCc494a810f    AIR    AIR.N        AIR     XNYS      NYS      US      USD      EQ          cs       COM USD1           False            True             US               US                    US   namr  2001119  000361105  US0003611052     1750.0          2585895.0       168154.0  001004  01          AIR US  BBG000BBGQF1  BBG000BBGQF1       AIR          U           780         72943               145         QG1FM5-R         WHQNFK-S       000BFS-E  H2SHPJHH8           2919.0             0     17747.0      30064827829         AIR  U-43477         50933.0       AIR            NYS 2022-05-04 04:59:57
    2  2022-05-04   784  ARS36894bbca  ARS36894bbca  ARCe6f2a8c15    ABB    ABB.N        ABB     XNYS      NYS      US      USD     ADR         adr  SPONSORED ADR           False            True             CH               CH                    CH   namr  2748472  000375204  US0003752047  1091587.0          2585899.0        18527.0  210418  91          ABB US  BBG000DK5Q25  BBG000DK5Q25  00037510          U           784         52570               145         G9ZKT1-R         PRM2JP-S       0036X2-E  TV4GK95L0           2676.0             0      3807.0      30064830118        BBOV    U-903         51405.0       ABB            NYS 2022-05-04 04:59:57
    3  2022-05-04   829  ARS4d332fd30  ARS4d332fd30  ARC2c0172027   ATSG  ATSG.OQ     ATSG.O     XNGS      NAS      US      USD      EQ          cs            COM           False            True             US               US                    US   namr  2938002  00922R105  US00922R1059   894081.0         44806861.0      3545047.0  155280  01         ATSG US  BBG000BLW5F7  BBG000BLW5F7     ABXAV          U           829         52542               135         L7HH56-R         SGHZ0K-S       071X8W-E  SMHT446B9           3288.0             0     51460.0      30064826978         ABX  U-75904          6091.0    ATSG.O            NAS 2022-05-04 04:59:57
    4  2022-05-04   835  ARS1f856790b  ARS1f856790b  ARCfad8ed944   ACCO   ACCO.N     ACCO.K     XNYS      NYS      US      USD      EQ          cs            COM           False            True             US               US                    US   namr  B0G7SZ5  00081T108  US00081T1088   712034.0         23428253.0      4184604.0  164506  02         ACCO US  BBG000J06K07  BBG000J06K07     ABDWI          U           835         70217               145         RPWCT1-R         R2KQ06-S       066M40-E  DPXVZQ4D0           2686.0             0    131582.0      30064826893        ABDW  U-96808         29276.0    ACCO.K            NYS 2022-05-04 04:59:57
    """

    df = pd.DataFrame()
    if preprocess_cols:
        modified_sql, ret_cols = _modify_sql(sql=sql, host=host, conn=conn,
                                             required_cols=required_cols, expected_cols=cols,
                                             quotes_on_colnames=quotes_on_colnames)
        if ret_cols:
            df = read_sql(sql=modified_sql, host=host, conn=conn)
    else:
        df = read_sql(sql=sql, host=host, conn=conn)
        ret_cols = _process_cols(available_cols=df.columns, required_cols=required_cols, expected_cols=cols,
                                 sql=sql)
        if ret_cols:
            df = df[ret_cols]

    if log_df_head:
        logger.info(f"Dataframe with shape {df.shape} returned from\n{sql}\nExamples:\n{df.head()}")

    return df


def create_upsert_method(db_code=None, schema=None,
                         meta: sqlalchemy.MetaData = None, extra_update_fields: Optional[Dict[str, str]] = None,
                         **db_config):
    """
    Create upsert method that satisfied the pandas's to_sql API.
    """

    if meta is None:
        if db_code is not None:
            host, port, user, password, database, db_type, db_name = _get_db_config(db_code=db_code)
            db_engine = _get_engine(db_type=db_type,
                                    host=host, port=port, user=user, password=password,
                                    database=database)
        else:
            db_type = db_config.get('db_type', 'POSTGRES')
            db_engine = get_os_env_engine(**db_config)

        meta = sqlalchemy.MetaData(db_engine)
        if schema is not None:
            meta.schema = schema

        if isinstance(db_type, str):
            db_type = DBType.retrieve(value=db_type)

    def method(table, conn, keys, data_iter):
        # select table that data is being inserted to (from pandas's context)
        sql_table = sqlalchemy.Table(table.name, meta, autoload=True)

        # list of dictionaries {col_name: value} of data to insert
        values_to_insert = [dict(zip(keys, data)) for data in data_iter]

        # create insert statement using postgresql dialect.
        # For other dialects, please refer to https://docs.sqlalchemy.org/en/14/dialects/

        if db_type==DBType.POSTGRES:
            insert_stmt = sqlalchemy.dialects.postgresql.insert(sql_table, values_to_insert)
        else:
            raise Exception(f'db_type={db_type} is not supported in [POSTGRES] !')

        # create update statement for excluded fields on conflict
        update_stmt = {exc_k.key: exc_k for exc_k in insert_stmt.excluded}
        if extra_update_fields:
            update_stmt.update(extra_update_fields)

        # create upsert statement.
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=sql_table.primary_key.columns,  # index elements are primary keys of a table
            set_=update_stmt  # the SET part of an INSERT statement
        )

        # execute upsert statement
        conn.execute(upsert_stmt)

    return method

@lru_cache
def get_os_env_engine(**db_config):
    db_type = db_config.get('db_type', 'POSTGRES')
    host, port, user, password, database = infer_db_config(db_code='DB', **db_config)

    engine = _get_engine(
        db_type=db_type,
        host=host,
        port=port,
        user=user,
        # password=cu.from_salted(secret_str=password),
        password=password,
        database=database
    )

    return engine


def get_os_env_conn(**db_config):
    engine = get_os_env_engine(**db_config)
    conn = engine.connect()

    return conn


def infer_db_config(db_code, **db_config):
    host = db_config.get(
        'host',
        ecfg.get_env_config().get(
            f'{db_code}.host',
            os.getenv(f'{db_code}_HOST', None)
        )
    )

    port = db_config.get(
        'port',
        ecfg.get_env_config().get(
            f'{db_code}.port',
            os.getenv(f'{db_code}_PORT', 9000)
        )
    )

    user = db_config.get(
        'user',
        ecfg.get_env_config().get(
            f'{db_code}.user',
            os.getenv(f'{db_code}_USER', 'default')
        )
    )

    password = db_config.get(
        'password',
        ecfg.get_env_config().get(
            f'{db_code}.password',
            os.getenv(f'{db_code}_PASSWORD', '')
        )
    )

    database = db_config.get(
        'database',
        ecfg.get_env_config().get(
            f'{db_code}.database',
            os.getenv(f'{db_code}_DATABASE', None)
        )
    )

    return host, port, user, password, database


def get_clickhouse_client(**db_config):
    db_code = db_config.pop('db_code') if 'db_code' in db_config else 'CH'
    host, port, user, password, database = infer_db_config(db_code=db_code, **db_config)
    #print(host, port, user, password)

    from clickhouse_driver import Client
    clickhouse_client = Client(host=host, port=int(port), user=user, password=password)

    return clickhouse_client


def persist_clickhouse_daily(data, cols, 
                             db_code, schema, table_name,
                             date_col='DateId',
                             delete_on_dates=True):
    col_names_str = '"' + '","'.join(cols) + '"'

    clickhouse_client = get_clickhouse_client(db_code=db_code)
    if delete_on_dates:
        dateids_db_str = mu.iterable_to_db_str(data[date_col].unique(), raw_type='int')
        sql = f'DELETE FROM "{schema}"."{table_name}" WHERE "DateId" IN {dateids_db_str}'
        clickhouse_client.execute(query=sql)

    sql = f'INSERT INTO "{schema}"."{table_name}" ({col_names_str}) VALUES'
    #print(sql)

    num_rows = clickhouse_client.insert_dataframe(
        query=sql,
        dataframe=data[cols],
        settings=dict(use_numpy=True),
    )

    sql = f'OPTIMIZE TABLE "{schema}"."{table_name}"'
    clickhouse_client.execute(query=sql)

    logger.info(f'{num_rows} rows inserted in "{schema}"."{table_name}" from data[cols].shape={data[cols].shape}!')