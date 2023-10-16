from abc import ABC
from dataclasses import dataclass
from qtc.consts.enums import (AssetClass, GicsLevel, Region, RiskModel, SignalValueType,
                              Frequency, SlippageType, ExecutionType, MissingHandlingType,
                              CostModelType, RiskDataTimestamp, Enum)
from qtc.app_configs.bq.constants import nb_day_year
from dataclasses import dataclass, fields
from typing import _GenericAlias, get_args, get_origin, Literal # type: ignore

@dataclass
class ReportParams(ABC):
    """
    Contains common report parameters
    """
    calc_custom_quantile_pnl: bool = False  #: 
    calc_lead_lag: bool = True  #: 
    calc_sector_exp: bool = True  #: 
    calc_sector_pnl: bool = True  #: 
    calc_country_pnl: bool = True  #: 
    calc_country_exp: bool = True  #: 
    calc_factor_exp: bool = True  #: 
    calc_factor_risk: bool = True  #: 
    calc_position_quantile_pnl: bool = True  #: 
    calc_volume_quantile_pnl: bool = True  #: 
    calc_fw_vol: bool = False  #: 
    calc_adv: bool = True  #: 
    calc_beta: bool = True  #: 
    calc_long_short_pnl: bool = True  #: 
    calc_earnings_pnl: bool = False  #: 
    calc_day_of_week_pnl: bool = True  #: 
    calc_quarterly_stats: bool = True  #: 
    calc_top_drawdown: bool = True  #: 
    calc_stock_bias: bool = True  #: 
    calc_factor_bias: bool = True  #: 
    calc_top_bottom_stock: bool = True  #:
    calc_top_factor: bool = True  #:
    calc_pnl_decomposition: bool = True  #: 
    calc_turnover: bool = True  #: 
    calc_position_stats: bool = True  #: 
    calc_trades_stats: bool = True  #: 
    calc_num_active_positions: bool = True  #: 
    calc_pnl: bool = True  #: 
    calc_accounting_costs: bool = True  #: 
    calc_exposures: bool = True  #: 
    calc_vol_hist_from_daily_pnl: bool = True  #: 
    calc_vol_hist_from_daily_factor_pnl: bool = True  #:
    calc_aggregate_accounting_stats: bool = True  #: 
    apply_holiday_adjustment: bool = False  #: 
    calc_market_cap_breakdown: bool = True  #

    vol_lookback_window: int = nb_day_year  #: 
    nb_top_bottom_stock: int = 50  #: number of stocks for which we want to report performance
    custom_quantile_bins: int = 5  #: number of bins for custom quantile pnl computation
    max_lead_days: int = 2  #: lead/lag pnl computation
    max_lag_days: int = 10  #: lead/lag pnl computation
    nb_top_drawdown: int = 10  #: number of drawdowns to report (sorted by depth)
    nb_day_significance_bias: int = nb_day_year  #: Do not report bias for stocks with few valid positions
    nb_stock_bias: int = 50  #: number of stocks for which we report the bias

    drift_pos: bool = True  #: account for positions drift; drift means that appreciation or depreciation in value doesn't cause trades

    gics_level: GicsLevel = GicsLevel.Sector  #: 
    
    risk_data_timestamp: RiskDataTimestamp = RiskDataTimestamp.pos_t  #: Shift risk data

    archive_run: bool = False  #: 
    
    execution_type: ExecutionType = ExecutionType.Vwap  #: 

    calc_dollar: bool = False  #: Set to True if want stats in dollars and not as percentage of gmv


@dataclass
class SignalParams(ABC):
    """
    Contains common signal parameters
    """
    asset_class: AssetClass = AssetClass.EQY  #: 
    region: Region = Region.US  #: 
    risk_model: RiskModel = RiskModel.AXUS4_MH  #: 
    signal_value_type: SignalValueType = SignalValueType.MoneyAllocation  #: 
    frequency: Frequency = Frequency.D1  #: 
    missing_dates_handling: MissingHandlingType = MissingHandlingType.Ignore  #:
    
@dataclass
class CostParamsBase(ABC):
    slippage_type: SlippageType = SlippageType.MarketImpact  #:
    cost_model_type: CostModelType = CostModelType.Equity  #: 


def dict2dataclass(cls, dict_args: dict):
    typed_dict = {}
    for f in fields(cls):
        if not f.init:
            continue
        
        value = dict_args.get(f.name)
        if value is None:
            continue
        if get_origin(f.type):
            if isinstance(value, dict):
                typed_dict[f.name] = get_args(f.type)[0](**value)
            else:
                typed_dict[f.name] = get_args(f.type)[0](value)
        else:
            typed_dict[f.name] = f.type(value)

    return cls(**typed_dict)


def dataclass2dict(cls) -> dict:
    res = {}
    for f in fields(cls):
        if not f.init:
            continue
        if issubclass(type(f.type), _GenericAlias):
            res[f.name] = getattr(cls, f.name)
        elif issubclass(f.type, Enum):
            res[f.name] = getattr(cls, f.name).value
        else:
            res[f.name] = getattr(cls, f.name)

    return res

