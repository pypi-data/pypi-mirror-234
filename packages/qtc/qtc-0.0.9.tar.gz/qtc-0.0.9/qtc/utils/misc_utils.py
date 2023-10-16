import numbers
from collections import OrderedDict
from typing import Iterable
import pandas as pd
from qtc.consts.enums import DollarDenominator, DecimalUnit


def iterable_to_tuple(items, raw_type, sep=',', remove_duplicates=True):
    """Converts "iterable" items into a tuple.

    :param items: Items to be converted. If str, have to be comma separated.
    :type items: str | numbers.Integral | Iterable
    :param raw_type: The data type in the result tuple. 'str' or 'int' are supported.
    :type raw_type: str
    :param sep: Seperator to split items if items is a str.
    :type sep: str
    :param remove_duplicates: To only keep unique items.
    :type remove_duplicates: bool
    :return: tuple

    >>> import qtc.utils.miscs_utils as mu
    >>> mu.iterable_to_tuple('5, 3,-1,3,5,9', raw_type='int')
    (5, 3, -1, 9)
    >>> mu.iterable_to_tuple('5, 3,-1,3,5,9', raw_type='int', remove_duplicates=False)
    (5, 3, -1, 3, 5, 9)
    >>> mu.iterable_to_tuple('Hello', raw_type='str')
    ('Hello',)
    >>> mu.iterable_to_tuple(pd.Series([4,-2,9]), raw_type='str')
    ('4', '-2', '9')
    """
    if isinstance(items, str):
        items = (item.strip() for item in items.split(sep))
        if remove_duplicates:
            items = OrderedDict.fromkeys(items).keys()
    elif isinstance(items, numbers.Integral):
        items = (items, )
    # elif not isinstance(items, list) and not isinstance(items, tuple) \
    #         and not isinstance(items, set) and not isinstance(items, pd.Series):
    elif not isinstance(items, Iterable):
        raise NotImplementedError("The type of parameter 'items' can be only str | numbers.Integral | Iterable")

    raw_type = raw_type.lower()
    if raw_type == 'int':
        items = tuple(int(item) for item in items)
    elif raw_type == 'str':
        items = tuple(str(item) for item in items)

    return items


def preprocess_iterable(items, raw_type, sep=',', remove_duplicates=True):
    if items is None:
        return None

    items = set(iterable_to_tuple(items, raw_type=raw_type, sep=sep, remove_duplicates=remove_duplicates))
    return None if len(items)==0 else items


def iterable_to_db_str(items, raw_type, remove_duplicates=True):
    """This function converts "iterable" items into a str with SQL syntax.

    :param items: Items to be converted. If str, have to be comma separated.
    :type items: str | int | Iterable
    :param raw_type: The data type indicated in the result str. 'str' or 'int' are supported.
    :type raw_type: str
    :param remove_duplicates: To only keep unique items.
    :type remove_duplicates: bool
    :return: str - Object with SQL syntax.

    >>> import qtc.utils.miscs_utils as mu
    >>> mu.iterable_to_db_str('5, 3,-1,3,5,9', raw_type='int')
    '(5,3,-1,9)'
    >>> mu.iterable_to_db_str('5, 3,-1,3,5,9', raw_type='int', remove_duplicates=False)
    '(5,3,-1,3,5,9)'
    >>> mu.iterable_to_db_str('Hello', raw_type='str')
    "('Hello')"
    >>> mu.iterable_to_db_str(pd.Series([4,-2,9]), raw_type='str')
    "('4','-2','9')"
    >>> mu.iterable_to_db_str('Hello, world', raw_type='str')
    "('Hello','world')"
    """
    items = iterable_to_tuple(items, raw_type, remove_duplicates=remove_duplicates)

    if len(items) == 0:
        raise Exception("Parameter 'items' should contain at least one element")

    # items = f"({items[0]})" if len(items) == 1 else str(items)
    if raw_type == 'int':
        items = f"({','.join((str(item) for item in items))})"
    else:
        items = "','".join(items)
        items = f"('{items}')"

    return items


def apply_dollar_denominator_on_df_cols(df, dollar_denominator, cols=None, inplace=False):
    if cols is None:
        return df

    if not inplace:
        df = df.copy()

    if isinstance(dollar_denominator, str):
        dollar_denominator = DollarDenominator.retrieve(value=dollar_denominator)

    for col in iterable_to_tuple(cols, raw_type='str'):
        if col in df.columns:
            if dollar_denominator==DollarDenominator.MILLION:
                df[col] /= 1e6

    return df


def apply_decimal_unit_on_df_cols(df, decimal_unit, cols=None, inplace=False):
    if cols is None:
        return df

    if not inplace:
        df = df.copy()

    if isinstance(decimal_unit, str):
        decimal_unit = DecimalUnit.retrieve(value=decimal_unit)

    for col in iterable_to_tuple(cols, raw_type='str'):
        if col in df.columns:
            if decimal_unit == DecimalUnit.PERCENTAGE:
                df[col] *= 1e+2
            elif decimal_unit == DecimalUnit.BPS:
                df[col] *= 1e+4
            elif decimal_unit != DecimalUnit.DECIMAL:
                raise Exception(f'decimal_unit={decimal_unit} is not supported in [DECIMAL | PERCENTAGE | BPS] !')

    return df


def post_normalize_df(df,
                      dollar_cols=None, decimal_cols=None,
                      dollar_denominator='MILLION', decimal_unit='DECIMAL',
                      inplace=False):
    if not inplace:
        df = df.copy()

    df = apply_dollar_denominator_on_df_cols(df=df, cols=dollar_cols,
                                             dollar_denominator=dollar_denominator, inplace=True)

    df = apply_decimal_unit_on_df_cols(df=df, cols=decimal_cols,
                                       decimal_unit=decimal_unit, inplace=True)

    return df


def standardize_col_names(cols):
    replace_map = {'Exposure': 'Exp',
                   'Variance': 'Var',
                   'Gmv': 'GMV',
                   'Nmv': 'NMV',
                   'Mv': 'MV',
                   'PNL': 'PnL',
                   'PL': 'PnL',
                   'AllocatedCapitalUnit': 'ACU'}

    def standardize_col_name(col):
        for k, v in replace_map.items():
            col = col.replace(k, v)

        return col

    return [standardize_col_name(col) for col in iterable_to_tuple(cols, raw_type='str')]


def get_zero_centered_min_max(values):
    if isinstance(values, list) or isinstance(values, tuple) or isinstance(values, set) or isinstance(values, pd.Series):
        values = list(values)
        min_val = min(values)
        max_val = max(values)
    elif isinstance(values, pd.DataFrame):
        min_val = values.min().min()
        max_val = values.max().max()

    tmp = max(abs(min_val), abs(max_val))
    min_val, max_val = -tmp, tmp
    if min_val == max_val:
        min_val = min_val - 0.0001
        max_val = max_val + 0.0001

    return min_val, max_val