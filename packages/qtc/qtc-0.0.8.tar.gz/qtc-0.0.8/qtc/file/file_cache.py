import os, inspect
import pandas as pd
from qtc.ext.configurable import Configurable
import qtc.file.file_manager as fileman
import qtc.utils.datetime_utils as dtu
from qtc.consts.enums import FileCacheNameFormat, FileCacheMode
from qtc.ext.logging import set_logger
logger = set_logger()


class FileCache(Configurable, fileman.FileManager):
    DEFAULT_CONFIG = {'file_cache_mode': FileCacheMode.DISABLED,
                      'file_cache_dir': os.getenv('FILE_CACHE_ROOT', default=None),
                      'file_cache_name': FileCacheNameFormat.FUNC_NAME_KWARGS,
                      'file_cache_protocol': 'CSV'}

    NAME = 'FILE_CACHE_FILE_MANAGER'
    DATETIME_FOLDERS_BUILDER = fileman.DateTimeFoldersBuilderManager.get(root='',
                                                                         datetime_folder_structure_mode='NON_DATETIME')

    def collect_defaults(self):
        self.defaults = dict()
        if self.func is None:
            return

        signature = inspect.signature(self.func)
        for name, p in signature.parameters.items():
            if p.default!=inspect._empty:
                self.defaults[name] = p.default

    def __init__(self, func=None, datetime_folders_builder=None, file_serializer_dict=None):
        Configurable.__init__(self)
        fileman.FileManager.__init__(self,
                                     datetime_folders_builder=datetime_folders_builder,
                                     file_serializer_dict=file_serializer_dict)
        self.func = func

        self.collect_defaults()

    def compile_file_cache_name(self, **kwargs):
        file_cache_name = self.config['file_cache_name']
        if isinstance(file_cache_name, str):
            try:
                file_cache_name = FileCacheNameFormat.retrieve(file_cache_name)
            except:
                pass

        if isinstance(file_cache_name, str):
            for k, v in kwargs.items():
                if v is None:
                    continue
                    
                if k in ['dateid','date']:
                    dateid = dtu.normalize_date_to_dateid(date=v)
                    for field in ['dateid', 'date']:
                        ks = '${' + field + '}'
                        file_cache_name = file_cache_name.replace(ks, str(dateid))
                else:
                    ks = '${' + k + '}'
                    file_cache_name = file_cache_name.replace(ks, str(v))

            return file_cache_name

        if file_cache_name==FileCacheNameFormat.FUNC_NAME:
            return self.func.__name__
        elif file_cache_name==FileCacheNameFormat.FUNC_NAME_DATEID:
            file_cache_name = self.func.__name__
            if 'dateid' in kwargs:
                file_cache_name += '.' + str(kwargs['dateid'])
            elif 'date' in kwargs:
                dateid = dtu.normalize_date_to_dateid(date=kwargs['date'])
                file_cache_name += '.' + str(dateid)

            return file_cache_name
        elif file_cache_name==FileCacheNameFormat.FUNC_NAME_KWARGS:
            file_cache_name = self.func.__name__
            for k in kwargs:
                file_cache_name += '.' + f'{k}={kwargs[k]}'

            return file_cache_name
        # if file_cache_name==FileCacheNameFormat.FUNC_NAME_KWARGS_DATEID:
        #     file_cache_name = self.func.__name__
        #     for k, v in kwargs.items():
        #         file_cache_name += '.' + f'{k}={v}'
        #     #
        #     if 'dateid' in kwargs:
        #         file_cache_name += '.' + kwargs['dateid']
        #     #
        #     return file_cache_name
        #
        else:
            raise

    def __call__(self, *args, **kwargs):
        self.config.update(self.defaults)
        keys_config, keys_non_config = self.update_config(**kwargs)
        keys_non_config = {k: self.config[k] for k in self.config if k not in FileCache.DEFAULT_CONFIG}

        file_cache_mode = self.config['file_cache_mode']
        if isinstance(file_cache_mode, str):
            file_cache_mode = FileCacheMode.retrieve(file_cache_mode)

        if file_cache_mode==FileCacheMode.DISABLED:
            logger.debug(f'Skipping file caching {self.func.__module__}.{self.func.__name__} since file_cache_mode={file_cache_mode} !')
            self.reset_config()
            return self.func(*args, **kwargs)

        root = self.config['file_cache_dir']
        if root is None:
            root = os.getcwd()

        file_manager = fileman.FileManagerRegistry.get(self.NAME, root=root)

        # file_cache_name = self.compile_file_cache_name(**{k: v for k,v in keys_non_config.items() if v is not None})
        file_cache_name = self.compile_file_cache_name(**{k: v for k, v in kwargs.items() if k in keys_non_config and v is not None})
        file_serializer = fileman.FileSerializerManager.get(filename_prefix=file_cache_name,
                                                            filename_dt_component_type='NON_DATETIME',
                                                            protocol=self.config['file_cache_protocol'],
                                                            index=False)

        # file_path = file_manager.search_file(file_serializer=file_serialier,
        #                                      dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
        #                                      extra_filename_components=None,
        #                                      allow_as_of=False,
        #                                      log_error=True)
        file_path = file_manager.compile_file_path(file_serializer=file_serializer,
                                                   dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                                                   extra_filename_components=None,
                                                   include_run_dt=True)

        if file_cache_mode==FileCacheMode.OVERWRITE:
            data = self.func(*args, **kwargs)
            file_path = file_manager.serialize(data=data,
                                               file_serializer=file_serializer,
                                               dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                                               extra_filename_components=None,
                                               include_run_dt=False)
            self.reset_config()
            return data

        if file_cache_mode == FileCacheMode.ENABLED:
            if not os.path.exists(file_path):
                logger.debug(f'FileCache does not exist ! Loading data ...')
                data = self.func(*args, **kwargs)
                file_path = file_manager.serialize(data=data,
                                                   file_serializer=file_serializer,
                                                   dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                                                   extra_filename_components=None,
                                                   include_run_dt=False)
            else:
                data = file_manager._deserialize(file_serializer=file_serializer,
                                                 dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                                                 extra_filename_components=None,
                                                 allow_as_of=False,
                                                 dt_col=None,
                                                 log_error=True)

            self.reset_config()
            return data

        if file_cache_mode==FileCacheMode.READONLY:
            if not os.path.exists(file_path):
                self.reset_config()
                raise Exception(f'FileCache {file_path} does not exist while file_cache_mode={file_cache_mode} !')

            data = file_manager._deserialize(file_serializer=file_serializer,
                                             dt=None, subfolders=None, is_subfolders_under_dt_folder=True,
                                             extra_filename_components=None,
                                             allow_as_of=False,
                                             dt_col=None,
                                             log_error=True)
            self.reset_config()
            return data

FileCache.register()


def get_meta():
    file_cache_mode_enums = FileCacheMode.get_meta()
    file_cache_mode_enums['EnumClass'] = 'FileCacheMode'
    file_cache_name_format_enums = FileCacheNameFormat.get_meta()
    file_cache_name_format_enums['EnumClass'] = 'FileCacheNameFormat'
    protocol_enums = fileman.FileSerializationProtocol.get_meta()
    protocol_enums = protocol_enums.loc[['CSV','PKL','PKL_GZ']]
    protocol_enums['EnumClass'] = 'FileSerializationProtocol'

    meta = pd.concat([file_cache_mode_enums,
                      file_cache_name_format_enums,
                      protocol_enums])
    meta.index.name = 'EnumName'
    return meta.reset_index().set_index(['EnumClass','EnumName'])