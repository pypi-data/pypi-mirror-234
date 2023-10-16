from abc import ABC
from bq_configs.enums import *
from dataclasses import dataclass, fields
from math import inf
from typing import Optional, _GenericAlias, get_args, get_origin  # type: ignore


@dataclass
class TradeRules:
    min_trade_dollar: float = 0.0  #: filters out all trades with $ value below min_trade_size
    max_trade_dollar: float = inf  #: $ amounts
    max_trade_adv: float = inf  #: percentage of ADV
    min_trade_risk: float = 0  #: if (trades * V * trades’)^0.5 < min_trade_risk then no trade
    

@dataclass
class OrderManagerParamsBase(ABC):
    trade_rules: Optional[TradeRules] = None  #: trade rules
    fill_type: FillType = FillType.Close  #: fill type
    pov_cap: float = 0.1  #: 


@dataclass
class PositionManagerParamsBase(ABC):
    drift_pos: bool = True  #: Account for position drift
    

@dataclass
class PortfolioOptimizationParamsBase(ABC):
    strategy: str = 'BAM-Example-TEST'  #: Strategy name
    
    optimizer_type: OptimizerType = OptimizerType.BAMOptimizer  #: For optimizer_type: 'bam_optimizer' for the cloud optimizer, "MOSEK" for the MOSEK solver through cvxpy
    opt_url: Optional[str] = None  #: url to cloud-based optimizer. Will try to use getenv('BAM_OPTIMIZER_URL') if explicit value is not provided
    
    # GMV
    target_gmv: float = 250e6  #: Target Gross Market Value
    nmv_as_fraction_gmv: float = inf  #: Net Market Value as fraction of GMV, ex.: 0.1 
    
    # Transaction Cost
    tc_spread_scale: float = 0  #: Transaction Cost, ex.: 0.000001
    market_impact_exponent: float = 1.0  #: FIXME need some validation for this number
    tc_scale: float = 0.0  #: Transaction Cost scale, if set to 0 then no transaction cost
    srisk_power: float = 0.0  #: 

    # Positions
    turnover_limit: float = inf  #: Cap on the sum of the absolute value of all trades as percentage of GMV, can be inf, ex.: 0.2
    position_fraction_adtv: float = inf  #: Cap for each position as percentage of ADV, ex.: 0.01 for 1%
    trade_fraction_adtv: float = inf  # Cap for each trade as percentage of ADV, ex.: 0.01 for 1%
    position_fraction_gmv: float = inf  #: Cap for each position as percentage of GMV, ex.: 0.1 for 10%

    # Risk
    factor_risk_penalty: float = 0  #: ex.: 3.0e-3
    srisk_penalty: float = 0  #: ex.: 1.0e-8
    srisk_floor: float = 0  # default to zero, not needed.

    # Alpha
    penalty_scale_distance_from_ideal: float = 0  #: Set to 0 if return optimization; set to non-zero for deviation from ideal optimization

    # Volatility
    portfolio_vol: float = 0  #: default to zero, not needed.
    upper_total_factor_vol: Optional[float] = None  #: 
    upper_total_idio_vol: Optional[float] = None  #: 
    upper_total_vol: Optional[float] = None  #: 

    # Other
    # TODO used in OptimizerInput only. Potential duplicated by scale down
    scale_factor: float = 1  #: unused, see below scale_down (rescale the problem when x is either very large or very small)
    post_opt_check: bool = True  #: For non BAMOptimizer optimizers, check if fulfilled the constraints within a threshold
    min_srisk_pct: float = 0  #: 80 means 80%, Ensures specific risk makes up at least this much percent of total risk. Set to 0 to not enable
    # trade_rules: dict = field(default_factory=lambda: {'no_trade_dow': 'Mon Tue Thr', 'no_trade_cal': None})  #: Unused
    scale_down: float = 1e6  #: Scale down factor. A typical value is 1e6, which scales down by that factor. This is an important tool to use if you find the run is crashing
    auto_scale: bool = True  #: Automatically set scale_down based on GMV
    mkt_impact_scale_factor: float = 1  #: If set to 0 then no Market Impact Transaction Cost

    signal_value_type: SignalValueType = SignalValueType.ExpectedReturns  #: 
    default_ba: float = 0.0015  #: The default value for bid ask in intraday
    
    backtest: bool = True  #: 

    custom_factors_src_path: str = None

    # Additional constraints
    pos_bounds_cols: Optional[tuple] = ('Id', 'PositionLB1', 'PositionUB1')  #: columns for DataFrame of additional position constraints
    pos_bounds_data: Optional[list] = None  #: $ amounts, e.g. [['BBG000B9XRY4', -1000000, 5000000]]
    factor_constraints_cols: Optional[tuple] = ('FactorId', 'Upper', 'Lower')  #: columns for DataFrame of additional factor constraints
    factor_constraints_data: Optional[list] = None  #: [["Market Sensitivity", 10000.0, -10000.0], ["Volatility", 10000.0, -50000.0], ["Exchange Rate Sensitivity", 20000.0, -20000.0]]
    factor_constraint_type: str = 'dollar'  # options: 'dollar', 'percent'. Percent if % target_gmv

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
        if isinstance(getattr(cls, f.name), TradeRules):
            res[f.name] = to_dict(getattr(cls, f.name))
        elif issubclass(type(f.type), _GenericAlias):
            res[f.name] = getattr(cls, f.name)
        elif issubclass(f.type, Enum):
            res[f.name] = getattr(cls, f.name).value
        else:
            res[f.name] = getattr(cls, f.name)

    return res


def to_dict(arg) -> dict:
    return {f.name: getattr(arg, f.name) for f in fields(arg)}

