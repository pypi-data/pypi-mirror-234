from joblib import Parallel, delayed
import qtc.utils.misc_utils as mu
import pandas as pd
import platform


def infer_joblib_backend(use_default=False):
    if use_default:
        return 'loky'

    os_type = platform.system()
    backend = 'threading' if 'Windows' in os_type else 'multiprocessing'
    # backend = 'multiprocessing'
    return backend


def run_multi_dateids_joblib(dateids, func,
                             concat_axis=None,
                             n_jobs=1,
                             **kwargs):
    dateids = mu.iterable_to_tuple(dateids, raw_type='int')
    backend = infer_joblib_backend()
    ret = Parallel(n_jobs=n_jobs, backend=backend)(delayed(function=func)(dateid=dateid, **kwargs)
                                                   for dateid in dateids)
    if concat_axis is not None:
        ret = pd.concat(ret, axis=concat_axis, sort=False)

    return ret


def run_multi_dts_joblib(dts, func,
                         concat_axis=None,
                         n_jobs=1,
                         **kwargs):
    dts = mu.iterable_to_tuple(dts, raw_type='int')
    backend = infer_joblib_backend()
    ret = Parallel(n_jobs=n_jobs, backend=backend)(delayed(function=func)(dt=dt, **kwargs)
                                                   for dt in dts)

    if concat_axis is not None:
        ret = pd.concat(ret, axis=concat_axis, sort=False)

    return ret
