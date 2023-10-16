import numpy as np
# Accounting annualization factors
nb_day_year = 252  #: average trading days in US
sqrt_nb_day_year = nb_day_year**0.5  #: square root of number of trading days

mkt_cap_bins = [-np.inf, 100e6, 200e6, 300e6, 1e9, 10e9, np.inf]
