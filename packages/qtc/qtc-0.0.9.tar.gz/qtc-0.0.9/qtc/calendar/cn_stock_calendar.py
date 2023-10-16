from functools import lru_cache
import qtc.data.dal.calendar as dalcal
import qtc.utils.datetime_utils as dtu
from qtc.calendar.calendar import Calendar
from qtc.ext.logging import set_logger
logger = set_logger()


class CNStockCalendar(Calendar):
    @staticmethod
    @lru_cache
    def _load_trading_dateids():
        """
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar
        >>> trading_dateids = CNStockCalendar._load_trading_dateids()
        >>> trading_dateids[:5]
        [19901219, 19901220, 19901221, 19901224, 19901225]
        """

        cal = dalcal.query_calendar(exchanges='SSE,SZSE')
        trading_dateids = sorted(list(set(cal['cal_date'])))

        return trading_dateids

    @staticmethod
    def _get_trading_dateids(start_dateid=None, end_dateid=None):
        """
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar
        >>> tuple(CNStockCalendar._get_trading_dateids(start_dateid=20190101, end_dateid=20190115))
        (20190102,
         20190103,
         20190104,
         20190107,
         20190108,
         20190109,
         20190110,
         20190111,
         20190114,
         20190115)
        """
        return Calendar._get_trading_dateids(
            trading_dateids=CNStockCalendar._load_trading_dateids(),
            start_dateid=start_dateid, end_dateid=end_dateid
        )

    @staticmethod
    def is_trading_date(dateid):
        """
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar
        >>> CNStockCalendar.is_trading_date(dateid=20211224)
        True
        >>> CNStockCalendar.is_trading_date(dateid=20230123)
        False
        >>> CNStockCalendar.is_trading_date(dateid=20230515)
        True
        """

        trading_dateids = CNStockCalendar._get_trading_dateids()
        return dateid in trading_dateids

    @staticmethod
    def prev_trading_dateid(dateid=None):
        """Gets the previous trading dateid given a specific exchange.
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar
        >>> CNStockCalendar.prev_trading_dateid(dateid=20230516)
        20230515
        """
        if dateid is None:
            dateid = dtu.curr_dateid()

        trading_dateids = CNStockCalendar._load_trading_dateids()
        return Calendar.prev_trading_dateid(dateid=dateid, trading_dateids=trading_dateids)

    @staticmethod
    def next_trading_dateid(dateid=None):
        """Gets the next trading dateid given a specific exchange.
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar
        >>> CNStockCalendar.next_trading_dateid(dateid=20230515)
        20230516
        >>> CNStockCalendar.next_trading_dateid(dateid=20230512)
        20230515
        >>> CNStockCalendar.next_trading_dateid(dateid=20230120)
        20230130
        """
        if dateid is None:
            dateid = dtu.curr_dateid()

        trading_dateids = CNStockCalendar._load_trading_dateids()
        return Calendar.next_trading_dateid(dateid=dateid, trading_dateids=trading_dateids)

    @staticmethod
    def shift_trading_days(dateid, offset):
        """Shifts trading dates by 'offset', which can be positive or negative.
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar 
        >>> CNStockCalendar.shift_trading_days(dateid=20230511, offset=2)
        20230515
        >>> CNStockCalendar.shift_trading_days(dateid=20230130, offset=-3)
        20230118
        """
        trading_dateids = CNStockCalendar._load_trading_dateids()
        return Calendar.shift_trading_days(dateid=dateid, trading_dateids=trading_dateids, offset=offset)

    @staticmethod
    def get_asof_trading_dateid(dateid=None,
                                timezone=Calendar.DEFAULT_TIME_ZONE):
        trading_dateids = CNStockCalendar._load_trading_dateids()
        return Calendar.get_asof_trading_dateid(trading_dateids=trading_dateids, dateid=dateid,
                                                timezone=timezone)

    @staticmethod
    def get_trading_dateids(start_date=None, end_date=None, dates=None):
        """This function is a helper function to infer trading dates based on the parameters.

        .. note::
            The inference logic is shown as below:
                #. If 'dates' is given, find a intersection between dates contained in 'dates' and the trading dates on given 'exchange'.
                #. If 'dates' is None, 'start_date' and 'end_date' have to be both valid dates and trading dates between 'start_date' and 'end_date' on give 'exchange' will be returned.

        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar
        >>> list(CNStockCalendar.get_trading_dateids(start_date=20230118, end_date=20230131))
        [20230118, 20230119, 20230120, 20230130, 20230131]
        >>> list(CNStockCalendar.get_trading_dateids(dates='20191101,20191102,20191103,20191104,20191105,20191106,20191107'))
        [20191101, 20191104, 20191105, 20191106, 20191107]
        """

        trading_dateids = CNStockCalendar._load_trading_dateids()
        return Calendar.get_trading_dateids(trading_dateids=trading_dateids,
                                            start_date=start_date, end_date=end_date, dates=dates)

    @staticmethod
    def infer_start_dateid_end_dateid(start_date=None, end_date=None, date_range_mode='SINGLE_DATE',
                                      default_ctd=False, timezone=Calendar.DEFAULT_TIME_ZONE):
        """
        >>> from qtc.calendar.cn_stock_calendar import CNStockCalendar 
        >>> CNStockCalendar.infer_start_dateid_end_dateid()
        >>> CNStockCalendar.infer_start_dateid_end_dateid(default_ctd=True)
        >>> CNStockCalendar.infer_start_dateid_end_dateid(end_date='CTD')
        >>> CNStockCalendar.infer_start_dateid_end_dateid(start_date=20200101, end_date='CTD')
        >>> CNStockCalendar.infer_start_dateid_end_dateid(start_date=20200101, end_date=20210926)
        >>> CNStockCalendar.infer_start_dateid_end_dateid(end_date=20210926, date_range_mode='5D')
        >>> CNStockCalendar.infer_start_dateid_end_dateid(end_date=20210930, date_range_mode='ROLLING_WEEK')
        >>> CNStockCalendar.infer_start_dateid_end_dateid(end_date=20210930, date_range_mode='MTD')
        """

        trading_dateids = CNStockCalendar._load_trading_dateids()
        return Calendar.infer_start_dateid_end_dateid(trading_dateids=trading_dateids,
                                                      start_date=start_date, end_date=end_date, date_range_mode=date_range_mode,
                                                      default_ctd=default_ctd, timezone=timezone)

    @staticmethod
    def infer_trading_dateids(start_date=None, end_date=None, date_range_mode='SINGLE_DATE'):
        trading_dateids = CNStockCalendar._load_trading_dateids()

        dateids, start_dateid, end_dateid = Calendar.infer_trading_dateids(
            trading_dateids=trading_dateids,
            start_date=start_date, end_date=end_date, date_range_mode=date_range_mode
        )

        return dateids, start_dateid, end_dateid

    @staticmethod
    def get_best_trading_dateid(dateid=None, timezone=None):
        if dateid is None:
            dateid = dtu.curr_dateid(timezone=timezone)

        if CNStockCalendar.is_trading_date(dateid=dateid):
            return dateid

        return CNStockCalendar.prev_trading_dateid(dateid=dateid)
