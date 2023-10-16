import os
import pickle
import gzip
import traceback
import pytz
import tempfile
import contextlib
import time
import pandas as pd
import datatable
from qtc.ext.enum import Enum
import qtc.utils.datetime_utils as dtu
import qtc.utils.misc_utils as mu
import qtc.utils.file_system_utils as fsu
from qtc.ext.logging import set_logger
logger = set_logger()


class DateTimeFolderStructureMode(Enum):
    NON_DATETIME = 'NON_DATETIME'
    DATEID = 'DateId'
    YEAR_MONTH = '%Y/%Y%m'
    YEAR_MONTH_DATEID = '%Y/%Y%m/%Y%m%d'
    YEAR_DATEID = '%Y/%Y%m%d'
    YEAR = '%Y'
    YEAR_MONTH_DATESTR_HYPHEN_SEP = '%Y/%Y-%m/%Y-%m-%d'
    DATEID_HYPHEN_TIMESTR = '%Y%m%d-%H%M%S'
    DATETIME_TIMEZONE = '%Y%m%dT%H%M%S%z'
    YEAR_MONTH_DATESTR_HYPHEN_SEP_DATEID_HYPHEN_TIMESTR = '%Y/%Y-%m/%Y-%m-%d/%Y%m%d-%H%M%S'
    CURRENT = 'current'


class DateTimeFoldersBuilder:
    @property
    def root(self):
        return self.__root

    # @root.setter
    # def root(self, root):
    #     self.__root = root
    # #

    @property
    def datetime_folder_structure_mode(self):
        return self.__datetime_folder_structure_mode

    # @datetime_folder_structure_mode.setter
    # def datetime_folder_structure_mode(self, datetime_folder_structure_mode):
    #     self.__datetime_folder_structure_mode = datetime_folder_structure_mode
    # #

    @property
    def timezone(self):
        return self.__timezone

    # @timezone.setter
    # def timezone(self, timezone):
    #     self.__timezone = timezone
    # #

    def __init__(self, root, datetime_folder_structure_mode, timezone=None):
        self.__root = root
        if isinstance(datetime_folder_structure_mode, str):
            datetime_folder_structure_mode = DateTimeFolderStructureMode.from_name(datetime_folder_structure_mode)

        self.__datetime_folder_structure_mode = datetime_folder_structure_mode

        if timezone is None:
            timezone = pytz.timezone('UTC')

        self.__timezone = pytz.timezone(timezone) if isinstance(timezone, str) else timezone

    def _get_dt_folder_structure(self, dt, subfolders=None):
        """
        >>> from qtc.file.file_serialization import DateTimeFoldersBuilder
        >>> dfm1 = DateTimeFoldersBuilder(root='/bam/aws/devel/quant_risk/dw/positions',
                                          datetime_folder_structure_mode='DATEID',
                                          timezone='America/New_York')
        >>> dfm1._get_dt_folder_structure(dt='20200806-094916')
        '/bam/aws/devel/quant_risk/dw/positions/20200806'
        >>> dfm2 = DateTimeFoldersBuilder(root='/mnt/rsk/Risk/EPA_Hist/POMO-ALL_EQUITY_ACUS',
                                          datetime_folder_structure_mode='YEAR_MONTH_DAY',
                                          timezone='UTC')
        >>> dfm2._get_dt_folder_structure(dt='20200806-094916')
        '/mnt/rsk/Risk/EPA_Hist/POMO-ALL_EQUITY_ACUS/2020/202008/20200806'
        >>> fss = DateTimeFoldersBuilder(root='/bam/aws/devel/quant_risk/dw/positions',
                                         datetime_folder_structure_mode='YEAR_MONTH_DATESTR_HYPHEN_SEP',
                                         timezone='UTC')
        >>> fss._get_dt_folder_structure(dt='20200806-094916')
        '/bam/aws/devel/quant_risk/dw/positions/2020/2020-08/2020-08-06'
        >>> fss = DateTimeFoldersBuilder(root='/bam/aws/devel/quant_risk/dw/positions',
                                         datetime_folder_structure_mode='DATETIME',
                                         timezone='UTC')
        '/bam/aws/devel/quant_risk/dw/positions/20200806-094916'
        >>> dfm3 = DateTimeFoldersBuilder(root='/mnt/rsk/Risk/ESQA/Intraday',
                                          datetime_folder_structure_mode='YEAR_MONTH_DATESTR_HYPHEN_SEP_DATEID_HYPHEN_TIMESTR',
                                          timezone='UTC')
        >>> dfm3._get_dt_folder_structure(dt='20220222-165800')
        '/mnt/rsk/Risk/ESQA/Intraday/2022/2022-02/2022-02-22/20220222-165800'
        """

        parent_folder = self.root
        if subfolders is not None:
            parent_folder = os.path.join(parent_folder, *mu.iterable_to_tuple(subfolders, raw_type='str'))

        dt = dtu.normalize_dt(dt=dt, timezone=self.timezone)

        if self.datetime_folder_structure_mode == DateTimeFolderStructureMode.NON_DATETIME:
            folder = parent_folder
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.DATEID:
            folder = os.path.join(parent_folder, dt.strftime('%Y%m%d'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.YEAR_MONTH:
            folder = os.path.join(parent_folder, dt.strftime('%Y'), dt.strftime('%Y%m'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.YEAR_MONTH_DATEID:
            folder = os.path.join(parent_folder, dt.strftime('%Y'), dt.strftime('%Y%m'), dt.strftime('%Y%m%d'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.YEAR_DATEID:
            folder = os.path.join(parent_folder, dt.strftime('%Y'), dt.strftime('%Y%m%d'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.YEAR:
            folder = os.path.join(parent_folder, dt.strftime('%Y'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.YEAR_MONTH_DATESTR_HYPHEN_SEP:
            folder = os.path.join(parent_folder, dt.strftime('%Y'), dt.strftime('%Y-%m'), dt.strftime('%Y-%m-%d'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.YEAR_MONTH_DATESTR_HYPHEN_SEP_DATEID_HYPHEN_TIMESTR:
            folder = os.path.join(parent_folder, dt.strftime('%Y'), dt.strftime('%Y-%m'), dt.strftime('%Y-%m-%d'), dt.strftime('%Y%m%d-%H%M%S'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.DATEID_HYPHEN_TIMESTR:
            folder = os.path.join(parent_folder, dt.strftime('%Y%m%d-%H%M%S'))
        elif self.datetime_folder_structure_mode == DateTimeFolderStructureMode.CURRENT:
            folder = os.path.join(parent_folder, 'current')

        return folder

    def compile_folder(self, dt=None, subfolders=None, is_subfolders_under_dt_folder=True):
        """
        >>> from qtc.file.file_serialization import DateTimeFoldersBuilder
        >>> fs = DateTimeFoldersBuilder(root='/bam/aws/devel/quant_risk/dw/positions',
                                        datetime_folder_structure_mode='DATEID',
                                        timezone='America/New_York')
        >>> from qtc.file.file_serialization import FileSerializer
        >>> fsd = FileSerializer(filename_prefix='factor_loadings',
                                 filename_dt_component_type='DATEID')
        >>> fs.compile_folder(file_serializer=fsd,
                              dt=20210929,
                              extra_filename_components='Archive,BARRA-USFASTD')
        """

        dt = dtu.normalize_dt(dt=dt, timezone=self.timezone)

        if is_subfolders_under_dt_folder:
            folder = self._get_dt_folder_structure(dt=dt)
            if subfolders is not None:
                folder = os.path.join(folder, *mu.iterable_to_tuple(subfolders, raw_type='str'))
        else:
            folder = self._get_dt_folder_structure(dt=dt, subfolders=subfolders)

        return folder

    def __repr__(self):
        return f"{type(self).__name__}(" \
               f"root='{self.root}', " \
               f"datetime_folder_structure_mode={self.datetime_folder_structure_mode}, " \
               f"timezone={self.timezone})"


class FileSerializationProtocol(Enum):
    TXT = 'txt'
    CSV = 'csv'
    PKL = 'pkl'
    PKL_GZ = 'pkl.gz'
    PICKLE = 'pickle'
    PICKLE_GZ = 'pickle.gz'
    LOG = 'log'
    HTML = 'html'
    FEATHER = 'feather'
    FTR = 'ftr'
    JAY = 'jay'
    JAY_GZ = 'jay.gz'
    PDF = 'pdf'

    @staticmethod
    def suffix(protocol):
        try:
            if isinstance(protocol, str):
                protocol = FileSerializationProtocol.retrieve(protocol)

            ret = protocol.value
        except:
            logger.warn(f'Faild to retrieve FileSerializationProtocol with value={protocol} !')
            ret = protocol

        return ret

    @staticmethod
    def protocol(suffix):
        if suffix.startswith('.'):
            suffix = suffix[1:]

        try:
            return FileSerializationProtocol(suffix.lower())
        except Exception as e:
            logger.warn(f"suffix={suffix} is not supported in [txt|csv|pkl|pkl.gz|html|feather|ftr']. Use pkl.gz by default! ")
            return FileSerializationProtocol.PICKLE_GZ


class FilenameDateTimeComponentType(Enum):
    NON_DATETIME = 'NON_DATETIME'
    DATEID = 'DateId'
    DATEID_HYPHEN_TIMESTR = '%Y%m%d-%H%M%S'
    DATEID_T_TIMESTR_OFFSETSTR = '%Y%m%dT%H%M%S%z'


@contextlib.contextmanager
def atomic_overwrite(file_path, folder=None, text=True, gzip_on=False):
    if folder is None:
        folder = os.path.dirname(file_path)

    if gzip_on:
        raise Exception(f'Not ready yet for gzip_on={gzip_on}!')
        # # fd, tmp_path = tempfile.mkstemp(dir=folder, text=text)
        # if text:
        #     fd = tempfile.NamedTemporaryFile(mode='w', dir=folder, delete=False)
        #     tmp_path = fd.name
        #     with gzip.open(tmp_path, mode='w') as f:
        #         yield f
        # else:
        #     fd = tempfile.NamedTemporaryFile(mode='w+b', dir=folder, delete=False)
        #     tmp_path = fd.name
        #     with gzip.GzipFile(filename=tmp_path, mode='wb') as f:
        #         yield f
    else:
        fd, tmp_path = tempfile.mkstemp(dir=folder, text=text)
        if text:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                yield f
        else:
            with os.fdopen(fd, 'wb') as f:
                yield f

    error_count = 0
    while True:
        try:
            os.replace(tmp_path, file_path)  # this will only happen if no exception was raised
            break
        except PermissionError as e:
            error_count += 1  # Error with replacing, likely being replaced by another process

            if (error_count >= 10):
                raise

            logger.debug(f'Failed writing {file_path} - waiting {error_count} seconds')
            time.sleep(1 * error_count)  # Sleep increasing amounts of time

    if error_count > 0:
        logger.warn(f'Failed writing {file_path} {error_count} times')


class FileSerializer:
    @property
    def filename_prefix(self):
        return self.__filename_prefix

    @property
    def filename_exclude_str(self):
        return self.__filename_exclude_str

    @property
    def filename_dt_component_type(self):
        return self.__filename_dt_component_type

    @property
    def protocol(self):
        return self.__protocol

    @property
    def suffix(self):
        return self.__suffix

    @property
    def filename_component_sep(self):
        return self.__filename_component_sep

    @property
    def kwargs(self):
        return self.__kwargs

    def __init__(self, filename_prefix,
                 filename_dt_component_type,
                 protocol='PKL.GZ',
                 filename_component_sep='.',
                 filename_exclude_str=None,
                 **kwargs):
        self.__filename_prefix = filename_prefix
        self.__filename_exclude_str = filename_exclude_str

        if isinstance(filename_dt_component_type, str):
            filename_dt_component_type = FilenameDateTimeComponentType.retrieve(filename_dt_component_type)

        self.__filename_dt_component_type = filename_dt_component_type

        if isinstance(protocol, str):
            protocol = FileSerializationProtocol.retrieve(protocol)

        self.__protocol = protocol

        self.__suffix = FileSerializationProtocol.suffix(self.protocol)
        self.__filename_component_sep = filename_component_sep
        self.__kwargs = kwargs

    def _get_file_dt_component(self, dt):
        if self.filename_dt_component_type == FilenameDateTimeComponentType.NON_DATETIME:
            filename_dt_component = None
        elif self.filename_dt_component_type == FilenameDateTimeComponentType.DATEID:
            filename_dt_component = str(dtu.datetime_to_dateid(date=dt))
        elif self.filename_dt_component_type == FilenameDateTimeComponentType.DATEID_HYPHEN_TIMESTR:
            filename_dt_component = dt.strftime('%Y%m%d-%H%M%S')
        elif self.filename_dt_component_type == FilenameDateTimeComponentType.DATEID_T_TIMESTR_OFFSETSTR:
            filename_dt_component = dt.strftime('%Y%m%dT%H%M%S%z')

        return filename_dt_component

    def compile_filename(self, dt=None,
                         extra_filename_components=None,
                         timezone=None, include_run_dt=False):
        """
        >>> from qtc.file.file_serialization import FileSerializer
        >>> fsd = FileSerializer(filename_prefix='factor_loadings',
                                 filename_dt_component_type='DATEID')
        >>> fsd.compile_filename(dt=20210929, extra_filename_components='Archive,AXUS4-MH')
        'factor_loadings.Archive.AXUS4-MH.20210929.pkl.gz'
        """

        dt = dtu.normalize_dt(dt=dt, timezone=timezone)

        if extra_filename_components is None:
            extra_filename_components = list()
        else:
            extra_filename_components = list(mu.iterable_to_tuple(extra_filename_components, raw_type='str'))

        filename_dt_component = self._get_file_dt_component(dt=dt)
        filename_components = [self.filename_prefix] + extra_filename_components
        if filename_dt_component is not None:
            filename_components.append(filename_dt_component)

        filename = self.filename_component_sep.join(filename_components)
        filename = f'{filename}.{self.suffix}'

        return filename

    def search_file(self, folder, dt=None,
                    extra_filename_components=None,
                    timezone=None, allow_as_of=False,
                    log_error=True):
        """
        >>> from qtc.file.file_serialization import FileSerializer
        >>> fsd = FileSerializer(filename_prefix='basket_decomp',
                                 filename_dt_component_type='DATEID',
                                 protocol='PICKLE_GZ')
        >>> from qtc.ext.path import quant_risk_dir
        >>> fsd.search_file(folder=quant_risk_dir('dw','basket_decomp','2021','202109','20210929'))
        '/bam/aws/devel/quant_risk/dw/basket_decomp/2021/202109/20210929/basket_decomp.20210929.pickle.gz'
        """
        if folder is None:
            raise Exception(f'Pleaes provide folder explicitly !')

        if dt is None:
            allow_as_of = True

        dt = dtu.normalize_dt(dt=dt, timezone=timezone)

        if extra_filename_components is None:
            extra_filename_components = list()
        else:
            extra_filename_components = list(mu.iterable_to_tuple(extra_filename_components, raw_type='str'))

        filename_components = [self.filename_prefix] + extra_filename_components
        if not allow_as_of:
            filename_dt_component = self._get_file_dt_component(dt=dt)
            if filename_dt_component is not None:
                filename_components.append(filename_dt_component)

        sep = f'{self.filename_component_sep}*'
        file_pattern = sep.join(filename_components)
        if len(filename_components)==1 and self.filename_dt_component_type!=FilenameDateTimeComponentType.NON_DATETIME:
            file_pattern += sep

        file_pattern = f'{file_pattern}.{self.suffix}'

        files = fsu.search_files_by_pattern(file_patten=file_pattern, folder=folder,
                                            exclude_str=self.filename_exclude_str)

        if allow_as_of:
            if self.filename_dt_component_type!=FilenameDateTimeComponentType.NON_DATETIME:
                files = [f for f in files if fsu.is_earlier(path=f.replace(f'.{self.suffix}',''),
                                                            target_dt=dt,
                                                            filename_sep=self.filename_component_sep, timezone=timezone)]
            if len(files)>=1:
                return sorted(files)[-1]
            else:
                if log_error:
                    logger.error(f'No file with pattern {file_pattern} as of {dt} found in {folder}!')

                return None
        else:
            if len(files)==1:
                return files[0]

            if len(files)==0:
                if log_error:
                    logger.error(f'Expecting exactly ONE file with pattern {file_pattern}. '
                                 f'However {len(files)} files found in {folder} !')
                return None

            if log_error:
                logger.warn(f'Expecting exactly ONE file with pattern {file_pattern}. '
                            f'Use the first one in the following {len(files)} files found in {folder} !\n{files}')

            return files[0]

    def _serialize(self, data, file_path):
        if data is None:
            logger.warn(f"data is None. Skip serializing '{self.filename_prefix}' -> {file_path}")
            return None

        dirname = os.path.dirname(file_path)
        if dirname is not None and dirname.strip()!='':
            os.makedirs(dirname, exist_ok=True)

        try:
            if self.protocol == FileSerializationProtocol.TXT or \
               self.protocol == FileSerializationProtocol.LOG or \
               self.protocol == FileSerializationProtocol.HTML:
                with atomic_overwrite(file_path=file_path, text=True, gzip_on=False) as fh:
                    fh.write(data)
            elif self.protocol == FileSerializationProtocol.CSV:
                with atomic_overwrite(file_path=file_path, text=True, gzip_on=False) as fh:
                    if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
                        data.to_csv(fh, **self.kwargs)
                    else:
                        fh.write(data)
            elif self.protocol == FileSerializationProtocol.PICKLE or \
                 self.protocol == FileSerializationProtocol.PKL:
                with atomic_overwrite(file_path=file_path, text=False, gzip_on=False) as fh:
                    pickle.dump(data, fh)
            elif self.protocol == FileSerializationProtocol.PICKLE_GZ or \
                 self.protocol == FileSerializationProtocol.PKL_GZ:
                # with atomic_overwrite(file_path=file_path, text=False, gzip_on=True) as fh:
                #     # pickle.dump(data, fh)
                #     temp = pickle.dumps(data)
                #     print(temp)
                #     fh.write(temp)
                # #
                with gzip.open(file_path, 'wb') as fh:
                    pickle.dump(data, fh)
            elif self.protocol == FileSerializationProtocol.FEATHER:
                with atomic_overwrite(file_path=file_path, text=False, gzip_on=False) as fh:
                    if not isinstance(data, pd.DataFrame) and not isinstance(data, pd.Series):
                        raise Exception(f'type(data)={type(data)} is not supported with protocol={self.protocol} !')

                    data.to_feather(fh, compression='uncompressed', **self.kwargs)
            elif self.protocol == FileSerializationProtocol.FTR:
                with atomic_overwrite(file_path=file_path, text=False, gzip_on=False) as fh:
                    if not isinstance(data, pd.DataFrame) and not isinstance(data, pd.Series):
                        raise Exception(f'type(data)={type(data)} is not supported with protocol={self.protocol} !')

                    data.to_feather(fh, compression='lz4', **self.kwargs)
            elif self.protocol == FileSerializationProtocol.JAY:
                with atomic_overwrite(file_path=file_path, text=False, gzip_on=False) as fh:
                    if not isinstance(data, pd.DataFrame) and not isinstance(data, pd.Series):
                        raise Exception(f'type(data)={type(data)} is not supported with protocol={self.protocol} !')

                    for col in data.columns:
                        if isinstance(data[col].dtype, pd.Int64Dtype):
                            data[col] = data[col].astype(float)

                    fh.write(datatable.Frame(data).to_jay())
            elif self.protocol == FileSerializationProtocol.JAY_GZ:
                with gzip.open(file_path, 'wb') as fh:
                    fh.write(datatable.Frame(data).to_jay())
            else:
                raise Exception(f'Serialization for protocol={self.protocol} not supported yet !')

            if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
                logger.info(f"'{self.filename_prefix}' with shape {data.shape} serialized -> {file_path}")
            elif isinstance(data, dict):
                logger.info(f"'{self.filename_prefix}' with keys {data.keys()} serialized -> {file_path}")
            else:
                logger.info(f"'{self.filename_prefix}' serialized -> {file_path}")

            return file_path
        except Exception as e:
            logger.error(f"Failed to serialize '{self.filename_prefix}' -> {file_path}")
            traceback.print_exc()
            return None

    def serialize(self, data,
                  folder=None,
                  dt=None,
                  extra_filename_components=None,
                  timezone=None,
                  include_run_dt=False):
        filename = self.compile_filename(dt=dt,
                                         extra_filename_components=extra_filename_components,
                                         timezone=timezone,
                                         include_run_dt=include_run_dt)
        file_path = filename if folder is None else os.path.join(folder, filename)

        return self._serialize(data=data, file_path=file_path)

    def _deserialize(self, file_path, log_error=False):
        data = None
        try:
            if self.protocol == FileSerializationProtocol.TXT or \
               self.protocol == FileSerializationProtocol.LOG or \
               self.protocol == FileSerializationProtocol.HTML:
                with open(file_path, 'rt') as fh:
                    data = fh.read()
            elif self.protocol == FileSerializationProtocol.CSV:
                kwargs = self.kwargs.copy()
                kwargs.pop('index', None)
                data = pd.read_csv(file_path, **kwargs)
            elif self.protocol == FileSerializationProtocol.PICKLE or \
                 self.protocol == FileSerializationProtocol.PKL:
                try:
                    data = pd.read_pickle(file_path)
                except:
                    with open(file_path, 'rb') as fh:
                        data = pickle.load(fh)
            elif self.protocol == FileSerializationProtocol.PICKLE_GZ or \
                 self.protocol == FileSerializationProtocol.PKL_GZ:
                try:
                    data = pd.read_pickle(file_path)
                except:
                    with gzip.open(file_path, 'rb') as fh:
                        data = pickle.load(fh)
            elif self.protocol == FileSerializationProtocol.FEATHER or \
                 self.protocol == FileSerializationProtocol.FTR:
                data = pd.read_feather(file_path)
            elif self.protocol == FileSerializationProtocol.JAY:
                data = datatable.fread(file_path).to_pandas()
            elif self.protocol == FileSerializationProtocol.JAY_GZ:
                with gzip.open(file_path, 'rb') as fh:
                    content = fh.read()
                data = datatable.fread(content).to_pandas()
            if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
                logger.info(f"'{self.filename_prefix}' with shape {data.shape} deserialized <- {file_path}")
            else:
                logger.info(f"'{self.filename_prefix}' deserialized <- {file_path}")
        except Exception as e:
            if log_error:
                logger.error(f"Failed to deserialize <- {file_path}")
                traceback.print_exc()

        return data

    def deserialize(self,
                    folder=None,
                    dt=None,
                    extra_filename_components=None,
                    timezone=None, allow_as_of=False,
                    log_error=True):
        file_path = self.search_file(folder=folder, dt=dt,
                                     extra_filename_components=extra_filename_components,
                                     timezone=timezone, allow_as_of=allow_as_of,
                                     log_error=log_error)
        return self._deserialize(file_path=file_path, log_error=log_error)

    def __repr__(self):
        return f"{type(self).__name__}(filename_prefix='{self.filename_prefix}', " \
               f"protocol={self.protocol}, " \
               f"filename_dt_component_type={self.filename_dt_component_type}, " \
               f"filename_component_sep='{self.filename_component_sep}')"


class DateTimeFoldersBuilderManager:
    __registry = dict()

    @classmethod
    def get(cls, root, datetime_folder_structure_mode, timezone=None):
        if root is None:
            raise Exception(f'Please provide root explicitly !')

        if isinstance(datetime_folder_structure_mode, str):
            datetime_folder_structure_mode = DateTimeFolderStructureMode.retrieve(datetime_folder_structure_mode)

        key = (root, datetime_folder_structure_mode, timezone)
        if key not in DateTimeFoldersBuilderManager.__registry:
            DateTimeFoldersBuilderManager.__registry[key] = DateTimeFoldersBuilder(root=root,
                                                                                   datetime_folder_structure_mode=datetime_folder_structure_mode,
                                                                                   timezone=timezone)
        # else:
        #     logger.warn(f'Skipping creating a new DateTimeFoldersHelper object since '
        #                 f'key=(root={root}, datetime_folder_structure_mode={datetime_folder_structure_mode}, timezone={timezone}) '
        #                 f'has been registered!')
        #
        return DateTimeFoldersBuilderManager.__registry[key]


class FileSerializerManager:
    __registry = dict()
    __named_registry = dict()

    @classmethod
    def get(cls, filename_prefix, filename_dt_component_type,
            protocol='PKL.GZ',
            filename_component_sep='.',
            filename_exclude_str=None,
            **kwargs):
        if isinstance(filename_dt_component_type, str):
            filename_dt_component_type = FilenameDateTimeComponentType.retrieve(filename_dt_component_type)

        if isinstance(protocol, str):
            protocol = FileSerializationProtocol.retrieve(protocol)

        key = (filename_prefix, filename_dt_component_type, protocol, filename_component_sep, filename_exclude_str)
        if key not in FileSerializerManager.__registry:
            FileSerializerManager.__registry[key] = \
                FileSerializer(filename_prefix=filename_prefix,
                               filename_dt_component_type=filename_dt_component_type,
                               protocol=protocol,
                               filename_component_sep=filename_component_sep,
                               filename_exclude_str=filename_exclude_str,
                               **kwargs)
        # else:
        #     logger.warn(f'Skipping creating a new FileSerializer object since '
        #                 f'key=(filename_prefix={filename_prefix}, filename_dt_component_type={filename_dt_component_type}, protocol={protocol}, filename_component_sep={filename_component_sep}) '
        #                 f'has been registered!')
        #
        return FileSerializerManager.__registry[key]

    @classmethod
    def get_by_name(cls, name, log_error=True):
        if name not in FileSerializerManager.__named_registry:
            if log_error:
                logger.error(f'Failed to find FileSerializer with name={name}! Please register your FileSerializer first!')

            return None

        return FileSerializerManager.__named_registry[name]

    @classmethod
    def register(cls, name, filename_prefix, filename_dt_component_type,
                 protocol='PKL.GZ',
                 filename_component_sep='.',
                 filename_exclude_str=None,
                 **kwargs):
        if name in FileSerializerManager.__named_registry:
            logger.error(f'name={name} exists in FileSerializerManager.__named_registry! Please choose another unique name!')
            return None

        FileSerializerManager.__named_registry[name] = FileSerializerManager.get(filename_prefix=filename_prefix,
                                                                                 filename_dt_component_type=filename_dt_component_type,
                                                                                 protocol=protocol,
                                                                                 filename_component_sep=filename_component_sep,
                                                                                 filename_exclude_str=filename_exclude_str
                                                                                 **kwargs)
        return FileSerializerManager.__named_registry[name]
