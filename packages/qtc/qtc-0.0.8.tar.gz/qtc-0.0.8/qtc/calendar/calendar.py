import bisect
import re
from dateutil.relativedelta import relativedelta
import qtc.utils.datetime_utils as dtu
import qtc.utils.misc_utils as mu
from qtc.consts.enums import OffsetDateType
from qtc.ext.enum import Enum
from qtc.ext.logging import set_logger
logger = set_logger()

class CalendarType(Enum):
    EXCHANGE = 'Exchange'
    CN_STOCK = 'CN_STOCK'


class Calendar:
    DEFAULT_TIME_ZONE = 'Asia/Shanghai'

    @staticmethod
    def _get_trading_dateids(trading_dateids, start_dateid=None, end_dateid=None):
        start_dateid = min(trading_dateids) if start_dateid is None else int(start_dateid)
        end_dateid = max(trading_dateids) if end_dateid is None else int(end_dateid)

        return (dateid for dateid in trading_dateids if dateid >= start_dateid and dateid <= end_dateid)

    @staticmethod
    def is_trading_date(dateid, trading_dateids):
        return dateid in trading_dateids

    @staticmethod
    def prev_trading_dateid(dateid, trading_dateids):
        if dateid <= trading_dateids[0]:
            logger.error(f'dateid={dateid} is on or earlier than the first dateid {trading_dateids[0]} !')
            return None

        i = bisect.bisect_left(trading_dateids, dateid)
        return trading_dateids[i - 1] if trading_dateids[i] in trading_dateids else trading_dateids[i]

    @staticmethod
    def next_trading_dateid(dateid, trading_dateids):
        if dateid >= trading_dateids[-1]:
            logger.error(f'dateid={dateid} is on or later than the last dateid {trading_dateids[-1]} !')
            return None

        i = bisect.bisect_right(trading_dateids, dateid)
        return trading_dateids[i]

    @staticmethod
    def shift_trading_days(dateid, trading_dateids, offset):
        if offset is None or not isinstance(offset, int):
            logger.warn(f"Skipping since 'offset' is not properly provided!")
            return dateid
        #
        shift_func = Calendar.prev_trading_dateid if offset <= 0 else Calendar.next_trading_dateid
        offset = abs(offset)

        for i in range(offset):
            dateid = shift_func(dateid=dateid, trading_dateids=trading_dateids)

        return dateid

    @staticmethod
    def get_asof_trading_dateid(trading_dateids, dateid=None,
                                timezone=DEFAULT_TIME_ZONE):
        if dateid is None:
            dateid = dtu.curr_dateid(timezone=timezone)

        return dateid if Calendar.is_trading_date(dateid=dateid, trading_dateids=trading_dateids) else \
               Calendar.prev_trading_dateid(dateid=dateid, trading_dateids=trading_dateids)

    @staticmethod
    def get_trading_dateids(trading_dateids, start_date=None, end_date=None, dates=None):
        if dates is None:
            if start_date is None or end_date is None:
                raise Exception(f'Please provide either "dates" or ("start_date", "end_date")')

            start_dateid = dtu.normalize_date_to_dateid(date=start_date)
            end_dateid = dtu.normalize_date_to_dateid(date=end_date)

            dateids = Calendar._get_trading_dateids(start_dateid=start_dateid, end_dateid=end_dateid,
                                                    trading_dateids=trading_dateids)
        else:
            dates = mu.iterable_to_tuple(dates, raw_type='int')
            dateids = list()
            for date in dates:
                dateid = dtu.normalize_date_to_dateid(date=date)
                if dateid in trading_dateids:
                    dateids.append(dateid)

        return list(dateids)

    @staticmethod
    def infer_offset_dateid(ref_date, offset_date, trading_dateids):
        ref_date = dtu.parse_datetime(dt=ref_date)

        if isinstance(offset_date, str):
            ndays_matched = re.match(r"([-+]?\d+)D$", offset_date, re.IGNORECASE)
            if ndays_matched is not None:
                ndays = int(ndays_matched.groups()[0])
                offset_date = Calendar.shift_trading_days(dateid=dtu.normalize_date_to_dateid(date=ref_date),
                                                          trading_dateids=trading_dateids,
                                                          offset=ndays)
            else:
                offset_date = OffsetDateType.retrieve(value=offset_date)

                if offset_date == OffsetDateType.CURR_MONTH_END:
                    offset_date = dtu.get_month_end(date=ref_date)
                elif offset_date == OffsetDateType.NEXT_MONTH_END:
                    date = ref_date.replace(year=ref_date.year + 1, month=1, day=1) if ref_date.month == 12 else \
                           ref_date.replace(month=ref_date.month + 1, day=1)
                    offset_date = dtu.get_month_end(date=date)
                else:
                    raise Exception(f'future_date={offset_date} not supported in [CME|NME|*D] !')

        offset_dateid = dtu.normalize_date_to_dateid(date=offset_date)
        if not Calendar.is_trading_date(dateid=offset_dateid, trading_dateids=trading_dateids):
            offset_dateid = Calendar.next_trading_dateid(dateid=offset_dateid, trading_dateids=trading_dateids)

        return offset_dateid

    @staticmethod
    def infer_start_dateid_end_dateid(trading_dateids,
                                      start_date=None, end_date=None, date_range_mode='SINGLE_DATE',
                                      default_ctd=False, timezone=DEFAULT_TIME_ZONE):

        curr_dateid = dtu.curr_dateid(timezone=timezone)
        if end_date is None:
            end_dateid = curr_dateid
            if not default_ctd:
                end_dateid = Calendar.prev_trading_dateid(dateid=end_dateid, trading_dateids=trading_dateids)
        else:
            if end_date == 'PTD':
                end_dateid = Calendar.prev_trading_dateid(dateid=curr_dateid, trading_dateids=trading_dateids)
            elif end_date == 'CTD':
                end_dateid = curr_dateid
            else:
                end_dateid = dtu.normalize_date_to_dateid(date=end_date)
                if not Calendar.is_trading_date(dateid=end_dateid, trading_dateids=trading_dateids):
                    end_dateid = Calendar.prev_trading_dateid(dateid=end_dateid, trading_dateids=trading_dateids)

        if start_date is not None:
            start_dateid = dtu.normalize_date_to_dateid(date=start_date)
            if not Calendar.is_trading_date(dateid=start_dateid, trading_dateids=trading_dateids):
                start_dateid = Calendar.next_trading_dateid(dateid=start_dateid, trading_dateids=trading_dateids)
            if start_dateid <= end_dateid:
                return start_dateid, end_dateid
            else:
                logger.warn(f"Inconsistency found: start_date={start_dateid} > end_date={end_dateid}. "
                            f"start_date will be inferred by date_range_mode={date_range_mode} instead.")

        ndays_matched = re.match(r"(\d+)D$", date_range_mode, re.IGNORECASE)
        nweeks_matched = re.match(r"(\d+)W$", date_range_mode, re.IGNORECASE)
        nmonths_matched = re.match(r"(\d+)M$", date_range_mode, re.IGNORECASE)

        if date_range_mode == 'SINGLE_DATE':
            start_dateid = end_dateid
        elif date_range_mode == 'ROLLING_WEEK':
            start_dateid = Calendar.shift_trading_days(dateid=end_dateid, trading_dateids=trading_dateids, offset=-4)
        elif date_range_mode == 'ROLLING_MONTH':
            start_date = dtu.dateid_to_datetime(dateid=end_dateid) - relativedelta(months=1)
            start_dateid = dtu.datetime_to_dateid(date=start_date)
            if not Calendar.is_trading_date(dateid=start_dateid, trading_dateids=trading_dateids):
                start_dateid = Calendar.next_trading_dateid(dateid=start_dateid, trading_dateids=trading_dateids)
        elif date_range_mode == 'MTD':
            start_dateid = int(end_dateid / 100.0) * 100 + 1
            if not Calendar.is_trading_date(dateid=start_dateid, trading_dateids=trading_dateids):
                start_dateid = Calendar.next_trading_dateid(dateid=start_dateid, trading_dateids=trading_dateids)
        elif ndays_matched is not None:
            ndays = int(ndays_matched.groups()[0])
            start_dateid = Calendar.shift_trading_days(dateid=end_dateid, trading_dateids=trading_dateids, offset=-(ndays-1))
        elif nweeks_matched is not None:
            ndays = int(nweeks_matched.groups()[0]) * 5
            start_dateid = Calendar.shift_trading_days(dateid=end_dateid, trading_dateids=trading_dateids, offset=-(ndays - 1))
        elif nmonths_matched is not None:
            nmonths = int(nmonths_matched.groups()[0])
            start_date = dtu.dateid_to_datetime(dateid=end_dateid) - relativedelta(months=nmonths)
            start_dateid = dtu.datetime_to_dateid(date=start_date)
            if not Calendar.is_trading_date(dateid=start_dateid, trading_dateids=trading_dateids):
                start_dateid = Calendar.next_trading_dateid(dateid=start_dateid, trading_dateids=trading_dateids)
        else:
            raise Exception(f"Supported 'date_range_mode' are [SINGLE_DATE|ROLLING_WEEK|ROLLING_MONTH|MTD|$(ndays)D|$(nweeks)W|$(nmonths)M] !")

        return start_dateid, end_dateid

    @staticmethod
    def infer_trading_dateids(trading_dateids,
                              start_date=None, end_date=None, date_range_mode='SINGLE_DATE'):
        # start_dateid = None if start_date is None else dtu.normalize_date_to_dateid(date=start_date)
        # end_dateid = None if end_date is None else dtu.normalize_date_to_dateid(date=end_date)

        start_dateid, end_dateid = \
            Calendar.infer_start_dateid_end_dateid(trading_dateids=trading_dateids,
                                                   start_date=start_date, end_date=end_date,
                                                   date_range_mode=date_range_mode)
        dateids = list(Calendar.get_trading_dateids(trading_dateids=trading_dateids,
                                                    start_date=start_dateid, end_date=end_dateid))

        return dateids, start_dateid, end_dateid