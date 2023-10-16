import unittest, os
import pandas as pd
from qtc.file.file_cache import FileCache

BENCHMARK = pd.DataFrame({'Col1':[1, 2, 3],
                          'Col2': ['a', 'b', 'c']})

@FileCache
def load_data(dateid, factor_model_code,
              **kwargs):
    data = BENCHMARK
    return data


@FileCache
def load_data_new(date, factor_model_code,
                  file_cache_mode='l', file_cache_dir=None, file_cache_name='FUNC_NAME_DATEID', file_cache_protocol='CSV'):
    data = BENCHMARK
    return data


class TestFileCache(unittest.TestCase):
    def setUp(self) -> None:
        self.dateid = 20211019
        self.factor_model_code = 'BARRA-USFASTD'

    def test_file_cache_mode_disabled(self):
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_mode='DISABLED')
        pd.testing.assert_frame_equal(data, BENCHMARK)

    def test_file_cache_mode_overwrite_enabled(self):
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_mode='OVERWRITE')
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_mode='ENABLED')

        pd.testing.assert_frame_equal(data, BENCHMARK)

        os.remove(f'load_data.dateid={self.dateid}.factor_model_code={self.factor_model_code}.csv')

    def test_file_cache_name_func_name_dateid(self):
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='FUNC_NAME_DATEID',
                         file_cache_mode='OVERWRITE')
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='FUNC_NAME_DATEID',
                         file_cache_mode='ENABLED')

        pd.testing.assert_frame_equal(data, BENCHMARK)

        os.remove(f'load_data.{self.dateid}.csv')

    def test_file_cache_name_func_name_dateid_1(self):
        data = load_data_new(date=self.dateid,
                             factor_model_code=self.factor_model_code,
                             file_cache_mode='OVERWRITE')
        data = load_data_new(date=str(self.dateid),
                             factor_model_code=self.factor_model_code,
                             file_cache_mode='ENABLED')

        pd.testing.assert_frame_equal(data, BENCHMARK)

        os.remove(os.path.join(os.getcwd(), f'load_data_new.{self.dateid}.csv'))

    def test_file_cache_name_user_defined(self):
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='my_test_file_cache',
                         file_cache_mode='OVERWRITE')
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='my_test_file_cache',
                         file_cache_mode='ENABLED')

        pd.testing.assert_frame_equal(data, BENCHMARK)

        os.remove(f'my_test_file_cache.csv')

    def test_file_cache_protocol_pkl(self):
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='my_test_file_cache',
                         file_cache_protocol='PKL',
                         file_cache_mode='OVERWRITE')
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='my_test_file_cache',
                         file_cache_protocol='PKL',
                         file_cache_mode='ENABLED')

        pd.testing.assert_frame_equal(data, BENCHMARK)

        os.remove(f'my_test_file_cache.pkl')

    def test_file_cache_protocol_pkl_gz(self):
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='my_test_file_cache',
                         file_cache_protocol='PKL_GZ',
                         file_cache_mode='OVERWRITE')
        data = load_data(dateid=self.dateid,
                         factor_model_code=self.factor_model_code,
                         file_cache_name='my_test_file_cache',
                         file_cache_protocol='PKL_GZ',
                         file_cache_mode='ENABLED')

        pd.testing.assert_frame_equal(data, BENCHMARK)

        os.remove(f'my_test_file_cache.pkl.gz')


if __name__ == '__main__':
    unittest.main()
