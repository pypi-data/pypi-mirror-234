import unittest, os
import pandas as pd
from qtc.file.file_serialization import FileSerializer, FileSerializationProtocol


class TestFileSerialization(unittest.TestCase):
    def test_FileSerializationProtocol(self):
        self.assertEqual(FileSerializationProtocol.suffix('CSV'), 'csv')
        self.assertEqual(FileSerializationProtocol.protocol('.pkl.gz'), FileSerializationProtocol.PKL_GZ)

    def test_compile_filename(self):
        fsd = FileSerializer(filename_prefix='factor_loadings',
                             filename_dt_component_type='DATEID',
                             protocol='PKL.GZ')
        self.assertEqual(fsd.compile_filename(dt=20210929, extra_filename_components='Archive,AXUS4-MH'),
                         'factor_loadings.Archive.AXUS4-MH.20210929.pkl.gz')

        fsd = FileSerializer(filename_prefix='market_data',
                             filename_dt_component_type='DATEID_HYPHEN_TIMESTR',
                             protocol='html')
        self.assertEqual(fsd.compile_filename(dt='20210929-093000', timezone='America/New_York'),
                         'market_data.20210929-093000.html')

        fsd = FileSerializer(filename_prefix='returns',
                             filename_dt_component_type='DATEID_T_TIMESTR_OFFSETSTR',
                             protocol='PICKLE')
        self.assertEqual(fsd.compile_filename(dt='20210929-093000', timezone='America/New_York'),
                         'returns.20210929T093000-0400.pickle')

    def test_serialization_1(self):
        benchmark = 'This is a\nmultiline\ntext for test.'
        fsd = FileSerializer(filename_prefix='test_serialization_1',
                             filename_dt_component_type='NON_DATETIME',
                             protocol='TXT')
        extra_filename_components = 'local,test'
        file_path = fsd.serialize(data=benchmark, folder=None, extra_filename_components=extra_filename_components)
        file_path = os.path.abspath(file_path)
        target_file_path = fsd.search_file(folder=os.path.dirname(file_path), extra_filename_components=extra_filename_components)
        self.assertEqual(target_file_path, file_path)

        target = fsd.deserialize(folder=os.path.dirname(file_path), extra_filename_components=extra_filename_components)
        self.assertEqual(target, benchmark)

        os.remove(file_path)

    def test_serialization_2(self):
        benchmark = pd.DataFrame({'Col1':[1,2,3], 'Col2':['a','b','c']}, index=['Row1','Row2','Row3'])
        fsd = FileSerializer(filename_prefix='test_serialization_2',
                             filename_dt_component_type='DATEID',
                             protocol='PKL_GZ')
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark')
        dt = 20210930
        file_path = fsd.serialize(data=benchmark, folder=folder, dt=dt)
        target_file_path = fsd.search_file(folder=folder, dt=dt)
        self.assertEqual(target_file_path, file_path)

        target = fsd.deserialize(folder=os.path.dirname(file_path), dt=dt)
        pd.testing.assert_frame_equal(target, benchmark)

        os.remove(file_path)

    def test_serialization_3(self):
        benchmark = pd.DataFrame({'Col1':[1,2,3], 'Col2':['a','b','c']}, index=['Row1','Row2','Row3'])
        benchmark.reset_index(inplace=True)
        fsd = FileSerializer(filename_prefix='test_serialization_3',
                             filename_dt_component_type='DATEID',
                             protocol='FEATHER')
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark')
        dt = 20210930
        file_path = fsd.serialize(data=benchmark, folder=folder, dt=dt)
        target_file_path = fsd.search_file(folder=folder, dt=dt)
        self.assertEqual(target_file_path, file_path)

        target = fsd.deserialize(folder=os.path.dirname(file_path), dt=dt)
        pd.testing.assert_frame_equal(target, benchmark)

        os.remove(file_path)

    def test_serialization_4(self):
        benchmark = pd.DataFrame({'Col1':[1,2,3], 'Col2':['a','b','c']}, index=['Row1','Row2','Row3'])
        benchmark.reset_index(inplace=True)
        fsd = FileSerializer(filename_prefix='test_serialization_4',
                             filename_dt_component_type='DATEID',
                             protocol='FTR')
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark')
        dt = 20210930
        file_path = fsd.serialize(data=benchmark, folder=folder, dt=dt)
        target_file_path = fsd.search_file(folder=folder, dt=dt)
        self.assertEqual(target_file_path, file_path)

        target = fsd.deserialize(folder=os.path.dirname(file_path), dt=dt)
        pd.testing.assert_frame_equal(target, benchmark)

        os.remove(file_path)

    def test_serialization_5(self):
        benchmark = pd.DataFrame({'Col1':[1,2,3], 'Col2':['a','b','c']}, index=['Row1','Row2','Row3'])
        benchmark.reset_index(inplace=True)
        fsd = FileSerializer(filename_prefix='test_serialization_5',
                             filename_dt_component_type='DATEID',
                             protocol='JAY')
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark')
        dt = 20220525
        file_path = fsd.serialize(data=benchmark, folder=folder, dt=dt)
        target_file_path = fsd.search_file(folder=folder, dt=dt)
        self.assertEqual(target_file_path, file_path)

        target = fsd.deserialize(folder=os.path.dirname(file_path), dt=dt)
        pd.testing.assert_frame_equal(target, benchmark)

        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
