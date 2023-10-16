import os
import pandas as pd


def get_swl1_config():
    """
    >>> from qtc.consts.static import get_swl1_config
    >>> swl1_config = get_swl1_config()
    >>> swl1_config.head()
      index_code industry_name level  industry_code  is_pub  parent_code     src factor_code
    0  801010.SI          农林牧渔    L1         110000       1            0  SW2021      SW2111
    1  801030.SI          基础化工    L1         220000       1            0  SW2021      SW2122
    2  801040.SI            钢铁    L1         230000       1            0  SW2021      SW2123
    3  801050.SI          有色金属    L1         240000       1            0  SW2021      SW2124
    4  801080.SI            电子    L1         270000       1            0  SW2021      SW2127
    """
    swl1_config_file = os.path.join(os.path.dirname(__file__), 'swl1.csv')
    swl1_config = pd.read_csv(swl1_config_file, encoding='gb18030')
    return swl1_config