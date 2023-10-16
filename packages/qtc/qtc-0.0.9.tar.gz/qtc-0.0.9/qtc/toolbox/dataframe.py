import pandas as pd
import qtc.utils.misc_utils as mu


def merge_dfs(df1, df2,
              key_cols='BookId,SecurityCode', data_cols='MV',
              how='outer',
              suffixes=('.DF1', '.DF2')):
    """
    >>> import qtc.toolbox.dataframe as tbdf
    >>> tbdf.merge_dfs(df1, df2, data_cols='MV')
    """
    key_cols = list(mu.iterable_to_tuple(key_cols, raw_type='str'))
    data_cols = list(mu.iterable_to_tuple(data_cols, raw_type='str'))

    cols = key_cols + data_cols
    df1 = pd.DataFrame(columns=cols) if df1 is None else df1[cols]
    df2 = pd.DataFrame(columns=cols) if df2 is None else df2[cols]

    merged = pd.merge(df1, df2,
                      on=key_cols, how=how, suffixes=suffixes)
    for col in data_cols:
        for suffix in suffixes:
            merged[f'{col}{suffix}'].fillna(0, inplace=True)

    return merged