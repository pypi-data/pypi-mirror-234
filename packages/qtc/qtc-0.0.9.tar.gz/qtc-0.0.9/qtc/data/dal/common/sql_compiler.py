import qtc.utils.misc_utils as mu
import qtc.utils.datetime_utils as dtu


def build_dateid_sql_and_clauses(start_dateid=None, end_dateid=None, dateids=None,
                                 quotes_on_colnames=False):
    """
    >>> import qtc.data.dal.common.sql_compiler as sqlc
    >>> sqlc.build_dateid_sql_and_clauses(start_dateid=20200901)
    ['DateId>=20200901']
    >>> sqlc.build_dateid_sql_and_clauses(start_dateid=20200901, end_dateid=20200915)
    ['DateId>=20200901', 'DateId<=20200915']
    >>> sqlc.build_dateid_sql_and_clauses()
    []
    >>> sqlc.build_dateid_sql_and_clauses(dateids='20200901, 20200902, 20200903')
    ['DateId IN (20200901,20200902,20200903)']
    """
    dateid_sql_and_clauses = list()

    colname = '"DateId"' if quotes_on_colnames else 'DateId'
    if dateids is not None:
        dates_db_str = mu.iterable_to_db_str(dateids, raw_type='int')
        dateid_sql_and_clauses.append(f"{colname} IN {dates_db_str}")
    else:
        if start_dateid is not None:
            dateid_sql_and_clauses.append(f"{colname}>={start_dateid}")
        if end_dateid is not None:
            dateid_sql_and_clauses.append(f"{colname}<={end_dateid}")

    return dateid_sql_and_clauses
