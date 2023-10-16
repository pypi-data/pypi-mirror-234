import qtc.utils.datetime_utils as dtu
import qtc.utils.misc_utils as mu
import qtc.data.dal.sec as dalsec


def load_market(start_date=None, end_date=None,
                security_codes=None,
                cols=None):
    """
    >>> import qtc.data.sec as sec
    >>> sec.load_market(start_date=20230519, end_date=20230519,
                        security_codes='600123.SH,300383.SZ',
                        cols='Return1D')
         DateId SecurityCode  Return1D
    0  20230519    300383.SZ -0.000898
    1  20230519    600123.SH -0.005477
    """

    fields_map = {
        'trade_date': 'DateId',
        'ts_code': 'SecurityCode',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'pct_chg': 'Return1D',
        'vol': 'Volume',
        'amount': 'Amount',
        'adj_factor': 'AdjFactor'
    }

    if cols is not None:
        fields_map_reverse = {v:k for k,v in fields_map.items()}
        cols = [fields_map_reverse.get(col, col)
                for col in mu.iterable_to_tuple(cols, raw_type='str')]

    start_dateid = dtu.normalize_date_to_dateid(date=start_date)
    end_dateid = dtu.normalize_date_to_dateid(date=end_date)
    market = dalsec.query_market(
        start_dateid=start_dateid, end_dateid=end_dateid,
        security_codes=security_codes,
        cols=cols
    )

    if market is not None and len(market)>0:
        market.rename(columns=fields_map, inplace=True)
        if 'Return1D' in market.columns:
            market['Return1D'] /= 1e2

    return market
