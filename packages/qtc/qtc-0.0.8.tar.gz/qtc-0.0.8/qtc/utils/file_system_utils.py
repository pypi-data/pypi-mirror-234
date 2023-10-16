import os
import glob
import yaml
import qtc.utils.datetime_utils as dtu
from qtc.ext.logging import set_logger
logger = set_logger()


def extract_datetime_from_path(path, dt_index=None, filename_sep='.', timezone=None):
    """
    >>> import qtc.utils.file_system_utils as fsu
    >>> fsu.extract_datetime_from_path(path='$HOME/earnings.20211004.csv')
    datetime.datetime(2021, 10, 4, 0, 0)
    """
    dt = None
    try:
        components = os.path.basename(path).split(filename_sep)
        if dt_index is None:
            for component in components:
                try:
                    dt = dtu.parse_datetime(component, ret_as_timestamp=False, timezone=timezone)
                    break
                except:
                    continue
        else:
            dt = dtu.parse_datetime(components[dt_index], ret_as_timestamp=False, timezone=timezone)
    except Exception as e:
        logger.error(f'{path} not recognized as containing datetime component with '
                     f'dt_index={dt_index}, filename_sep={filename_sep}')
        return None

    return dt


def is_earlier(path, target_dt=None, dt_index=None, filename_sep='.', timezone=None):
    """
    >>> import qtc.utils.file_system_utils as fsu
    >>> fsu.is_earlier(path='${HOME}/market_data.20200901-210228.csv',
                       target_dt='20200901-210245')
    True
    >>> fsu.is_earlier(path='${HOME}/market_data_.20200901-210228.csv',
                       target_dt='20200901-210100')
    False
    """

    target_dt = dtu.normalize_dt(dt=target_dt, timezone=timezone)
    if target_dt is None:
        raise Exception(f'target_dt={target_dt} cannot be recognized as a valid datetime !')

    dt = extract_datetime_from_path(path=path, dt_index=dt_index, filename_sep=filename_sep, timezone=timezone)
    if dt is None:
        return False

    return dt <= target_dt


def list_datetime_subfolders(folder,
                             ret_abs_path=True, ascending=True, dt_no_later_than=None,
                             timezone=None):
    """
    >>> from qtc.ext.path import sysequity_dir
    >>> folder = sysequity_dir('Reports', 'Archive')
    >>> import qtc.utils.file_system_utils as fsu
    >>> fsu.list_datetime_subfolders(folder=folder)[:5]
    >>> fsu.list_datetime_subfolders(folder=folder, ret_abs_path=False)[:5]
    ['20160104', '20160105', '20160106', '20160107', '20160108']
    >>> fsu.list_datetime_subfolders(folder=folder, dt_no_later_than=20160105)
    >>> fsu.list_datetime_subfolders(folder=folder, ret_abs_path=False, ascending=False)[-5:]
    ['20160108', '20160107', '20160106', '20160105', '20160104']
    """
    def is_valid_datetime_folder(path, dt_no_later_than=None):
        if not os.path.isdir(path):
            return False

        dt = None
        try:
            subfolder = os.path.basename(path)
            dt = dtu.parse_datetime(subfolder, ret_as_timestamp=False)
        except Exception as e:
            logger.debug(f"Skipping '{subfolder}' since it is not a date subfolder! ")
            return False

        if dt_no_later_than is None:
            return True

        dt_no_later_than = dtu.normalize_dt(dt=dt_no_later_than, timezone=timezone)
        if dt_no_later_than is None:
            logger.warn(f'dt_no_later_than={dt_no_later_than} cannot be recognized as a valid datetime !')
            return True

        return dt <= dt_no_later_than

    if folder is None or folder.strip()=='' or not os.path.exists(folder):
        return None

    if dt_no_later_than is not None:
        dt_no_later_than = dtu.normalize_dt(dt=dt_no_later_than, timezone=timezone)

    ret = [os.path.join(folder, subfolder) if ret_abs_path else subfolder
           for subfolder in os.listdir(folder) if is_valid_datetime_folder(os.path.join(folder, subfolder),
                                                                           dt_no_later_than=dt_no_later_than)]
    ret.sort(reverse=not ascending)

    return ret


def search_files_by_pattern(file_patten, folder=None, exclude_str=None):
    """
    >>> from qtc.ext.path import sysequity_dir
    >>> folder = quant_risk_dir('EPA_Hist', 'Archive', '20160104')
    >>> import qtc.utils.file_system_utils as fsu
    >>> fsu.search_files_by_pattern(file_patten='summary.*.*.pickle.gz', folder=folder)
    """
    if folder is not None:
        file_patten = os.path.join(folder, file_patten)

    files = glob.glob(file_patten)

    return files if exclude_str is None else [file for file in files if exclude_str not in file]


def search_single_file_by_pattern(file_patten, folder=None, log_error=True):
    """
    >>> from qtc.ext.path import sysequity_dir
    >>> folder = sysequity_dir('EPA_Hist', 'Archive', '20160104')
    >>> import qtc.utils.file_system_utils as fsu
    >>> fsu.search_single_file_by_pattern(file_patten='summary_GICS_IndustrySector.*.*.pickle.gz', folder=folder)
    >>> fsu.search_single_file_by_pattern(file_patten='test.*.*.pickle.gz', folder=folder)

    """
    files = search_files_by_pattern(file_patten=file_patten, folder=folder)
    if len(files) != 1:
        if log_error:
            logger.error(f"Expecting exactly ONE file with pattern: {file_patten} in folder={folder}, "
                         f"however found {len(files)} !")
        return None

    return files[0]


def read_yaml_config_recursively(yaml_config_file):
    if yaml_config_file is None:
        return None

    config_main = None
    try:
        with open(yaml_config_file) as fh:
            config_main = yaml.safe_load(fh, Loader=yaml.FullLoader)
    except Exception as e:
        logger.error(f"Failed to load yaml config from {yaml_config_file}:\n{e}")
        return None

    includes = config_main.get('includes', None)
    config_from_includes = None
    if includes is not None and len(includes) > 0:
        config_from_includes = dict()
        for include in includes:
            include_yaml_config_file = include if os.path.exists(include) else os.path.join(os.path.dirname(yaml_config_file), include)
            config_from_include = read_yaml_config_recursively(yaml_config_file=include_yaml_config_file)
            if config_from_include is not None:
                config_from_includes.update(config_from_include)

    config = dict() if config_from_includes is None else config_from_includes

    if config_main is not None:
        config.update(config_main)

    return config
