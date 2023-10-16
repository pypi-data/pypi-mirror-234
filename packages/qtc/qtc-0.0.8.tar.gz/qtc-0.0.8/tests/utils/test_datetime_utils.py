import pandas as pd
from datetime import datetime
import pytz
import qtc.utils.datetime_utils as dtu
import qtc.ext.unittest as ut


class TestDateTimeUtils(ut.TestCase):
    def test_datetime_to_dateid(self):
        self.assertEqual(dtu.datetime_to_dateid(datetime(2020, 11, 25)), 20201125)
        adt = datetime(2020, 8, 7, 2, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(dtu.datetime_to_dateid(adt), 20200807)
        self.assertEqual(dtu.datetime_to_dateid(adt.astimezone(pytz.timezone('America/New_York'))), 20200806)

    def test_dateid_to_datetime(self):
        self.assertEqual(dtu.dateid_to_datetime(20190925), datetime(2019, 9, 25, 0, 0))
        self.assertEqual(dtu.dateid_to_datetime(20190925, timezone='America/New_York'), datetime(2019, 9, 25, 0, 0, tzinfo=pytz.timezone('America/New_York')))

    def test_dateid_to_datestr(self):
        self.assertEqual(dtu.dateid_to_datestr(20201124), '2020-11-24')
        self.assertEqual(dtu.dateid_to_datestr(20201124, sep='/'), '2020/11/24')

    def test_today(self):
        self.assertEqual(dtu.curr_dateid(), dtu.datetime_to_dateid(datetime.now()))
        self.assertEqual(dtu.curr_dateid(timezone='Asia/Tokyo'), dtu.datetime_to_dateid(datetime.now(pytz.timezone('Asia/Tokyo'))))
        self.assertEqual(dtu.curr_dateid(timezone='Europe/London'), dtu.datetime_to_dateid(datetime.now(pytz.timezone('Europe/London'))))
        self.assertEqual(dtu.curr_dateid(timezone='America/New_York'), dtu.datetime_to_dateid(datetime.now(pytz.timezone('America/New_York'))))

    def test_is_weekday(self):
        self.assertEqual(dtu.is_weekday(20200511), True)
        self.assertEqual(dtu.is_weekday(20201128), False)

    def test_get_biz_dates(self):
        self.assertEqual(dtu.get_biz_dateids(start_date=20201120, end_date=20201129), [20201120, 20201123, 20201124, 20201125, 20201126, 20201127])

    def test_next_biz_date(self):
        self.assertEqual(dtu.next_biz_dateid(dateid=20201125), 20201126)
        self.assertEqual(dtu.next_biz_dateid(dateid=20201127), 20201130)

    def test_parse_datetime(self):
        self.assertEqual(dtu.parse_datetime(20200210), datetime(2020, 2, 10, 0, 0))
        self.assertEqual(dtu.parse_datetime('2020-11-25', ret_as_timestamp=True), pd.Timestamp('2020-11-25 00:00:00'))

        target = dtu.parse_datetime('20200210-164523', timezone='America/New_York')
        benchmark = datetime(2020, 2, 10, 16, 45, 23, tzinfo=pytz.timezone('America/New_York'))
        self.assertEqual(target.strftime('%Y%m%d-%H%M%d'), benchmark.strftime('%Y%m%d-%H%M%d'))

        target = dtu.parse_datetime('2020/02/10 16:45:23', format='%Y/%m/%d %H:%M:%S', timezone='Asia/Shanghai')
        benchmark = datetime(2020, 2, 10, 16, 45, 23, tzinfo=pytz.timezone('Asia/Shanghai'))
        self.assertEqual(target.strftime('%Y%m%d-%H%M%d'), benchmark.strftime('%Y%m%d-%H%M%d'))

    def test_normalize_date_to_dateid(self):
        self.assertEqual(dtu.normalize_date_to_dateid(date=20210929), 20210929)
        self.assertEqual(dtu.normalize_date_to_dateid(date='2021-09-29'), 20210929)
        self.assertEqual(dtu.normalize_date_to_dateid(datetime(2021,9,29)), 20210929)

    def test_convert_data_type_for_date_col(self):
        benchmark = self.load_benchmark(basename='convert_data_type_for_date_col.param1.csv',
                                        parse_dates=['Date'])
        data = dtu.convert_data_type_for_date_col(pd.DataFrame({'DateId':[20210927,20210928,20210929]}), date_col='DateId')
        pd.testing.assert_frame_equal(data.head(), benchmark)

    def test_get_week_start_dateid(self):
        self.assertEqual(dtu.get_week_start_dateid(date=20220526), 20220523)
        self.assertEqual(dtu.get_week_start_dateid(date=20220522), 20220516)
        self.assertEqual(dtu.get_week_start_dateid(date=20220523), 20220523)


if __name__ == '__main__':
    ut.main()
