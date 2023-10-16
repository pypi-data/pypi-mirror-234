import os
import shutil
import pandas as pd
import qtc.ext.unittest as ut
import qtc.file.file_manager as fileman


class CustomFileManager(fileman.FileManager):
    NAME = 'CUSTOM_FILE_MANAGER'
    DATETIME_FOLDERS_BUILDER = fileman.DateTimeFoldersBuilderManager.get(
        root=os.path.join(os.path.dirname(__file__), 'test_custom_file_manager'),
        datetime_folder_structure_mode='DATEID',
        timezone='America/New_York')
    FILE_SERIALIZER_DICT = {'POSITIONS': fileman.FileSerializerManager.get(filename_prefix='positions',
                                                                           filename_dt_component_type='DATEID',
                                                                           protocol='PKL.GZ',
                                                                           filename_component_sep='.')}
CustomFileManager.register()


class TestFileManager(ut.TestCase):
    def test_get_meta(self):
        benchmark = self.load_benchmark(basename='file_manager_meta.csv')
        benchmark.set_index(['EnumClass','EnumName'], inplace=True)
        pd.testing.assert_frame_equal(fileman.get_meta(), benchmark)

    def test_file_manager_serialization(self):
        cfm = fileman.FileManagerRegistry.get('CUSTOM_FILE_MANAGER')

        data = pd.DataFrame({'SecurityId': [409, 2654], 'NMV': [-10, 10]})
        file_path = cfm.serialize(data=data,
                                  file_serializer='POSITIONS',
                                  dt=20210929,
                                  subfolders=None,
                                  extra_filename_components=None,
                                  include_run_dt=False)
        data = pd.DataFrame({'SecurityId': [409,2654], 'NMV': [-20,20]})
        file_path = cfm.serialize(data=data,
                                  file_serializer='POSITIONS',
                                  dt=20210930,
                                  subfolders=None,
                                  extra_filename_components=None,
                                  include_run_dt=False)

        target = cfm.deserialize(file_serializer='POSITIONS',
                                 start_dt=20210901, end_dt=20210930,
                                 subfolders=None,
                                 extra_filename_components=None,
                                 allow_as_of=False,
                                 dt_type='DateId')

        benchmark = self.load_benchmark(basename='deserialization.param1.csv')
        pd.testing.assert_frame_equal(target, benchmark)

        target = cfm.deserialize(file_serializer='POSITIONS',
                                 dts='20210929,20210930',
                                 subfolders=None,
                                 extra_filename_components=None,
                                 allow_as_of=False,
                                 dt_type='DateId')
        pd.testing.assert_frame_equal(target, benchmark)

        # test_data_root = sysequity_dir('test_custom_file_manager')
        test_data_root = cfm.root#'test_custom_file_manager'
        shutil.rmtree(test_data_root)


if __name__ == '__main__':
    ut.main()
