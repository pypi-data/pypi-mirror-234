import os
import pandas as pd
from joblib import Parallel, delayed
import qtc.utils.datetime_utils as dtu
import qtc.utils.misc_utils as mu
from qtc.consts.enums import DateDataType
from qtc.ext.multiprocessing import infer_joblib_backend
from qtc.file.file_serialization import \
    DateTimeFolderStructureMode, FilenameDateTimeComponentType, FileSerializationProtocol, \
    DateTimeFoldersBuilder, FileSerializer, DateTimeFoldersBuilderManager, FileSerializerManager
from qtc.ext.logging import set_logger
logger = set_logger()


class FileManager:
    @classmethod
    def register(cls):
        if not hasattr(cls, 'NAME'):
            logger.warn(f"Skipping since no class variable 'NAME' in {cls} !")
            return None

        if cls.NAME is None:
            logger.warn(f"Skipping since {cls}.NAME is None !")

        if not hasattr(cls, 'DATETIME_FOLDERS_BUILDER'):
            logger.warn(f"Skipping since no class variable 'DATETIME_FOLDERS_BUILDER' in {cls} !")
            return None

        if cls.DATETIME_FOLDERS_BUILDER is None or not isinstance(cls.DATETIME_FOLDERS_BUILDER, DateTimeFoldersBuilder):
            logger.warn(f"Skipping since {cls}.DATETIME_FOLDER_BUILDER is None or not of type DateTimeFoldersBuilder !")

        file_serializer_dict = None
        if hasattr(cls, 'FILE_SERIALIZER_DICT'):
            file_serializer_dict = cls.FILE_SERIALIZER_DICT

        FileManagerRegistry.register(name=cls.NAME,
                                     file_manager_cls=cls,
                                     datetime_folders_builder=cls.DATETIME_FOLDERS_BUILDER,
                                     file_serializer_dict=file_serializer_dict)

    @property
    def datetime_folders_builder(self):
        return self.__datetime_folders_builder

    @datetime_folders_builder.setter
    def datetime_folders_builder(self, datetime_folders_builder):
        self.__datetime_folders_builder = datetime_folders_builder

    @property
    def file_serializer_dict(self):
        return self.__file_serializer_dict

    @file_serializer_dict.setter
    def file_serializer_dict(self, file_serializer_dict):
        self.__file_serializer_dict = file_serializer_dict

    @property
    def root(self):
        return self.datetime_folders_builder.root

    @property
    def datetime_folder_structure_mode(self):
        return self.datetime_folders_builder.datetime_folder_structure_mode

    # def __init__(self, name,
    #              root, datetime_folder_structure_mode,
    #              filename_prefix, filename_dt_component_type,
    #              protocol='PKL.GZ',
    #              filename_component_sep='.',
    #              timezone=None,
    #              **kwargs):
    #     self.datetime_folders_builder = None
    #     self.file_serializers = list()
    # #

    def __init__(self, datetime_folders_builder, file_serializer_dict=None):
        if datetime_folders_builder is not None:
            if not isinstance(datetime_folders_builder, DateTimeFoldersBuilder):
                raise Exception(f'datetime_folders_builder={datetime_folders_builder} is not of type DateTimeFoldersBuilder !')

        self.datetime_folders_builder = datetime_folders_builder

        self.file_serializer_dict = dict()
        if file_serializer_dict is not None:
            if not isinstance(file_serializer_dict, dict):
                raise Exception(f'file_serializer_dict={file_serializer_dict} has to be of type dict(key:str, value:DateTimeFoldersBuilder) !')

            for name, file_serializer in file_serializer_dict.items():
                if not isinstance(file_serializer, FileSerializer):
                    logger.warn(f'With name={name}, file_serializer={file_serializer} is not of type FileSerializer!')
                    continue

                self.file_serializer_dict[name] = file_serializer

    def get_file_serializer(self, file_serializer):
        if isinstance(file_serializer, str):
            if file_serializer not in self.file_serializer_dict:
                file_serializer_from_registry = FileSerializerManager.get_by_name(name=file_serializer, log_error=False)
                if file_serializer_from_registry is None:
                    logger.error(f'No file_serializer with name={file_serializer} neither in this class object nor global FileSerializerManager!')
                    return None
                else:
                    return file_serializer_from_registry
            else:
                return self.file_serializer_dict[file_serializer]
        elif isinstance(file_serializer, FileSerializer):
            return file_serializer

        logger.warn(f'file_serializer={file_serializer} is not a str nor a FileSerializer !')
        return None

    def __repr__(self):
        class_variables_repr = '\n\t'
        datetime_folders_builder_class = None
        file_serializer_dict_class = None
        # print(type(self))
        if hasattr(type(self), 'NAME'):
            class_variables_repr += f'NAME: {type(self).NAME}' + '\n\t'
        if hasattr(type(self), 'DATETIME_FOLDERS_BUILDER'):
            datetime_folders_builder_class = type(self).DATETIME_FOLDERS_BUILDER
            class_variables_repr += f'DATETIME_FOLDERS_BUILDER: {datetime_folders_builder_class}' + '\n\t'
        if hasattr(type(self), 'FILE_SERIALIZER_DICT'):
            file_serializer_dict_class =  type(self).FILE_SERIALIZER_DICT
            class_variables_repr += f'FILE_SERIALIZER_DICT: {file_serializer_dict_class}' + '\n\t'

        repr = f'{type(self).__name__}({class_variables_repr}' \
               f'\n\tdatetime_folders_builder: {self.datetime_folders_builder if self.datetime_folders_builder!=datetime_folders_builder_class else "DATETIME_FOLDERS_BUILDER"}'\
               f'\n\tfile_serializer_dict: {self.file_serializer_dict if self.file_serializer_dict!=file_serializer_dict_class else "FILE_SERIALIZER_DICT"}'\
               f'\n)'
        return repr

    def compile_folder(self, dt, subfolders=None, is_subfolders_under_dt_folder=True):
        folder = self.datetime_folders_builder.compile_folder(dt=dt, subfolders=subfolders,
                                                              is_subfolders_under_dt_folder=is_subfolders_under_dt_folder)
        return folder

    def compile_file_path(self, file_serializer,
                          dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                          extra_filename_components=None,
                          include_run_dt=False):

        file_serializer = self.get_file_serializer(file_serializer=file_serializer)

        if file_serializer is None:
            raise Exception(f'Failed to obtain a FileSerializer instance!')

        folder = self.compile_folder(dt=dt, subfolders=subfolders,
                                     is_subfolders_under_dt_folder=is_subfolders_under_dt_folder)

        filename = file_serializer.compile_filename(dt=dt,
                                                    extra_filename_components=extra_filename_components,
                                                    timezone=self.datetime_folders_builder.timezone,
                                                    include_run_dt=include_run_dt)
        return os.path.join(folder, filename)

    def serialize(self, data,
                  file_serializer,
                  dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                  extra_filename_components=None,
                  include_run_dt=False):
        file_serializer = self.get_file_serializer(file_serializer=file_serializer)

        if file_serializer is None:
            raise Exception(f'Failed to obtain a FileSerializer instance!')

        file_path = self.compile_file_path(file_serializer=file_serializer,
                                           dt=dt, subfolders=subfolders, is_subfolders_under_dt_folder=is_subfolders_under_dt_folder,
                                           extra_filename_components=extra_filename_components,
                                           include_run_dt=include_run_dt)
        file_path = file_serializer._serialize(data=data, file_path=file_path)
        return file_path

    def search_file(self, file_serializer,
                    dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                    extra_filename_components=None,
                    allow_as_of=False,
                    log_error=True):
        file_serializer = self.get_file_serializer(file_serializer=file_serializer)

        if file_serializer is None:
            raise Exception(f'Failed to obtain a FileSerializer instance!')

        folder = self.compile_folder(dt=dt, subfolders=subfolders,
                                     is_subfolders_under_dt_folder=is_subfolders_under_dt_folder)
        filename = file_serializer.search_file(folder=folder,
                                               dt=dt,
                                               extra_filename_components=extra_filename_components,
                                               timezone=self.datetime_folders_builder.timezone, allow_as_of=allow_as_of,
                                               log_error=log_error)
        if filename is None:
            return None

        return os.path.join(folder, filename)

    def _deserialize(self, file_serializer,
                     dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                     extra_filename_components=None,
                     allow_as_of=False,
                     dt_col=None,
                     log_error=True,
                     ret_filepath=False,
                     **kwargs):
        file_serializer = self.get_file_serializer(file_serializer=file_serializer)

        file_path = kwargs.get('file_path', None)
        if file_path is None:
            file_path = self.search_file(file_serializer=file_serializer,
                                         dt=dt, subfolders=subfolders, is_subfolders_under_dt_folder=is_subfolders_under_dt_folder,
                                         extra_filename_components=extra_filename_components,
                                         allow_as_of=allow_as_of,
                                         log_error=log_error)

        data = file_serializer._deserialize(file_path=file_path, log_error=log_error)

        try:
            if dt_col is not None and dt_col not in data.columns:
                data[dt_col] = dtu.normalize_dt(dt=dt, timezone=self.datetime_folders_builder.timezone)
        except:
            pass

        return (data, file_path) if ret_filepath else data

    def deserialize(self, file_serializer,
                    start_dt=None, end_dt=None, dts=None,
                    subfolders=None,
                    extra_filename_components=None,
                    allow_as_of=False,
                    dt_type='DateId',
                    log_error=False,
                    to_df=True,
                    **kwargs):

        if isinstance(dt_type, str):
            dt_type = DateDataType.retrieve(dt_type)

        if dts is None:
            if dt_type == DateDataType.DATEID:
                dts = list(dtu.get_biz_dateids(start_date=start_dt, end_date=end_dt))
        else:
            dts = list(mu.iterable_to_tuple(dts, raw_type='str'))
            if dt_type==DateDataType.DATEID:
                dts = [dtu.datetime_to_dateid(dtu.normalize_dt(dt, timezone=self.datetime_folders_builder.timezone))
                       for dt in dts]

        dt_col = 'DateTime'
        file_serializer = self.get_file_serializer(file_serializer=file_serializer)
        backend = infer_joblib_backend()
        ret = Parallel(n_jobs=-1, backend=backend)(delayed(unwrap_FileManager_self__deserialize)\
                                                           (i,
                                                            file_serializer=file_serializer,
                                                            subfolders=subfolders,
                                                            extra_filename_components=extra_filename_components,
                                                            allow_as_of=allow_as_of,
                                                            dt_col=dt_col,
                                                            log_error=log_error,
                                                            **kwargs)
                                                   for i in zip([self]*len(dts), dts))
        ret = [item for item in ret if item is not None]
        if len(ret)==0:
            return None

        if to_df:
            ret = pd.concat(ret, ignore_index=True, sort=False)

            if dt_type==DateDataType.DATEID:
                ret = dtu.convert_data_type_for_date_col(df=ret, date_col=dt_col,
                                                         from_data_type=DateDataType.TIMESTAMP,
                                                         to_data_type=DateDataType.DATEID,
                                                         to_date_col_idx=None)
                ret.drop(columns=[dt_col], inplace=True)

        return ret


### Have to do it in this ugly way coz joblib is not able to handle locals in class obj
def unwrap_FileManager_self__deserialize(arg, **kwarg):
    return FileManager._deserialize(arg[0], **dict(kwarg, dt=arg[1]))


class FileManagerRegistry:
    __registry = dict()

    @classmethod
    def register(cls, name, file_manager_cls, datetime_folders_builder, file_serializer_dict=None):
        if name not in FileManagerRegistry.__registry:
            FileManagerRegistry.__registry[name] = file_manager_cls(datetime_folders_builder=datetime_folders_builder,
                                                                    file_serializer_dict=file_serializer_dict)
        else:
            logger.error(f'NAME has been registered for:\n{FileManagerRegistry.__registry[name]}')

        return FileManagerRegistry.__registry[name]

    # @classmethod
    # def initialize(cls):
    #     for subclass in FileManager.__subclasses__():
    #         logger.debug(f'Registering subclass: {subclass}')
    #         subclass.register()
    #         logger.debug(f'subclass: {subclass} successfully registered.')
    #     #
    # #

    @classmethod
    def get(cls, name, root=None):
        if name not in FileManagerRegistry.__registry:
            raise Exception(f'name={name} not found in FileManagerRegistry.registry !')

        file_manager = FileManagerRegistry.__registry[name]
        if root is None or root==file_manager.datetime_folders_builder.root:
            return file_manager

        datetime_folders_builder = DateTimeFoldersBuilderManager.get(root=root,
                                                                     datetime_folder_structure_mode=file_manager.datetime_folders_builder.datetime_folder_structure_mode,
                                                                     timezone=file_manager.datetime_folders_builder.timezone)
        file_manager = type(file_manager)(datetime_folders_builder=datetime_folders_builder,
                                          file_serializer_dict=file_manager.file_serializer_dict)
        return file_manager


def get_meta():
    datetime_folder_structure_mode_enums = DateTimeFolderStructureMode.get_meta()
    datetime_folder_structure_mode_enums['EnumClass'] = 'DateTimeFolderStructureMode'
    filename_dt_component_type_enums = FilenameDateTimeComponentType.get_meta()
    filename_dt_component_type_enums['EnumClass'] = 'FilenameDateTimeComponentType'
    protocol_enums = FileSerializationProtocol.get_meta()
    protocol_enums['EnumClass'] = 'FileSerializationProtocol'

    meta = pd.concat([datetime_folder_structure_mode_enums,
                      filename_dt_component_type_enums,
                      protocol_enums])
    meta.index.name = 'EnumName'
    return meta.reset_index().set_index(['EnumClass','EnumName'])
