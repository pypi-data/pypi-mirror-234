from qtc.ext.enum import Enum


class DataTransmissionProtocol(Enum):
    TXT = 'txt'
    JSON = 'json'
    PICKLE = 'pickle'
    XML = 'xml'


class DollarDenominator(Enum):
    ONE = 'one'
    MILLION = 'million'


class DecimalUnit(Enum):
    DECIMAL = 'decimal'
    PERCENTAGE = '%'
    PERCENTAGE_SQUARE = '%^2'
    BPS = 'bps'


class DateDataType(Enum):
    DATEID = 'DateId'
    DATESTR = 'DateStr'
    TIMESTAMP = 'Date'
    DATETIME = 'Date'


class DataSource(Enum):
    DATABASE = 'DB'
    FMS = 'FMS'
    FILE_CACHE = 'FC'
    RERDSP = 'RERDSP'
    API = 'API'


class FileCacheNameFormat(Enum):
    FUNC_NAME = 'func_name'
    FUNC_NAME_DATEID = 'func_name.dateid'
    FUNC_NAME_KWARGS = 'func_name.kwargs'
    # FUNC_NAME_KWARGS_DATEID = 'func_name.kwargs.dateid'


class FileCacheMode(Enum):
    DISABLED = 'd'
    OVERWRITE = 'w'
    ENABLED = 'e'
    READONLY = 'r'


class Color(Enum):
    DARK_BLUE = '#002c56'
    MID_BLUE = '#1F4E78'
    LIGHT_BLUE = '#2e75b6'
    ORANGE = '#ff6328'
    GREY = '#939598'
    BLACK = '#000000'
    WHITE = '#FFFFFF'


class EntityType(Enum):
    ACUG = 'AllocatedCapitalUnitGroup'
    ACU = 'AllocatedCapitalUnit'
    STRAT = 'Strategy'


class DBType(Enum):
    MSSQL = 'MSSQL'
    REDSHIFT = 'REDSHIFT'
    POSTGRES = 'POSTGRES'
    MYSQL = 'MYSQL'


class Symbology(Enum):
    AXIOMA_ID = 'AxiomaId'
    BARRA_ID = 'BarraId'
    FIGI = 'FIGI'
    CFIGI = 'CFIGI'
    DISPLAY_CODE = 'DisplayCode'
    TICKER = 'Ticker'
    TICKER_EXCH = 'TickerExch'


class FactorIdentifier(Enum):
    FACTOR_ID = 'FactorId'
    FACTOR_DESC = 'FactorDesc'
    FACTOR_DESC_ID = 'FactorDesc=FactorId'
    FACTOR_CODE = 'FactorCode'


class UniverseMnemonic(Enum):
    SP500 = 'SP500'
    DOW30 = 'DOW30'
    NASDAQ100 = 'NASDAQ100'
    RUSSELL1000 = 'R1000'
    RUSSELL2000 = 'R2000'
    RUSSELL3000 = 'R3000'


class OffsetDateType(Enum):
    CURR_MONTH_END = 'CME'
    NEXT_MONTH_END = 'NME'


class TradingRegion(Enum):
    US = 'US'
    EU = 'EU'
    AP = 'Asia'
    ALL = 'ALL'
    RAW = 'Raw'


class CrossSectionalDataFormat(Enum):
    MATRIX = 'matrix'
    NARROW = 'narrow'


class BasketDecompMode(Enum):
    TOP_DOWN = 'lookthru'
    BOTTOM_UP = 'BOTTOM_UP'



from enum import Enum, unique


# ALPHA STORE
@unique
class ConfigsAttribution(Enum):
    BQ_SRF = 'BQ_SRF'
    BQ_SIM = 'BQ_SIM'


@unique
class ServerType(Enum):
    PROD = 'URL_PROD'
    DEV = 'URL_DEV'
    UAT = 'URL_UAT'
    

@unique
class AssetClass(Enum):
    CREDIT = 'CREDIT'
    EQY = 'EQY'
    FI = 'FI'  #: Fixed Income
    FUT = 'FUT'
    FUTOUTRIGHT = 'FUTOUTRIGHT'
    FX = 'FX'  #: Currencies
    OPTIONS = 'OPTIONS'
    EQY_FUT = 'EQY_FUT'  #: Combined Equity and Futures
    EQY_FUT_FX = 'EQY_FUT_FX'  #: Combined Equity, Futures and FX
    EQY_FX = 'EQY_FX'  #: Combined Equity and FX
    FUT_FX = 'FUT_FX'  #: Combined Futures and FX


@unique
class Frequency(Enum):
    D1 = 'D1'
    D0 = 'D0'
    INT_1min = 'INT_1min'
    INT_5min = 'INT_5min'
    EVENT = 'EVENT'
    IRREGULAR = 'IRREGULAR'
    HOURLY = 'HOURLY'


@unique
class Region(Enum):
    US = 'US'
    EU = 'EU'
    AS = 'AS'
    GL = 'GL'
    EU_ARIES_ID = 'EU_ARIES_ID'


@unique
class RiskModel(Enum):
    AXUS4_MH = 'AXUS4_MH'
    AXUS4_SH = 'AXUS4_SH'
    BARRA_USSLOWS = 'BARRA_USSLOWS'
    BARRA_USSINTM1L = 'BARRA_USSINTM1L'
    BARRA_USFASTD = 'BARRA_USFASTD'
    AXEU4_MH = 'AXEU4_MH'
    AXEU4_SH = 'AXEU4_SH'
    AXEU4_SH_ARIES_ID = 'AXEU4_SH_ARIES_ID'
    AXAP21_MH = 'AXAP21_MH'
    AXAP21_SH = 'AXAP21_SH'
    AXAP4_MH = 'AXAP4_MH'
    AXAP4_SH = 'AXAP4_SH'
    BARRA_ASE2S = 'BARRA_ASE2S'
    AXWW4_MH = 'AXWW4_MH'
    AXWW21_MH = 'AXWW21_MH'
    BARRA_GEMLTS = 'BARRA_GEMLTS'
    NONE = 'NONE'


@unique
class IdsType(Enum):
    CFIGI = 'CFIGI'
    CUSIP = 'CUSIP'
    SEDOL = 'SEDOL'
    TICKER = 'TICKER'
    ARIESID = 'ARIESID'
    SECURITYID = 'SECURITYID'
    MIXED = 'MIXED' 


# NB! Duplicated
@unique
class SignalType(Enum):
    """
    Units/meaning for the VALUE field in an alpha
    """
    SIGNAL = 'SIGNAL'
    POSITION = 'POSITION'
    SHARES = 'SHARES'
    ORDERS = 'ORDERS'
    

@unique
class UploadMethod(Enum):
    """
    Upload methods:
    insert - creates an alpha if it does not exist
    update - updates existing alpha
    overwrite - overwrites the existing alpha or creates one if it does not exist
    """
    insert = 'insert'
    update = 'update'
    overwrite = 'overwrite'


@unique
class DestinationType(Enum):
    staging = 'staging'
    prod = 'prod'
    

@unique 
class Role(Enum):
    User = 'user'
    Superuser = 'superuser'
    AlphaCapture = 'alpha_capture'
    Admin = 'admin'
    

@unique
class Status(Enum):
    RESEARCH = 'RESEARCH'
    TESTING = 'TESTING'
    LIVE = 'LIVE'
    DEPRECATED = 'DEPRECATED'


@unique
class SlippageType(Enum):
    MarketImpact = 'market_impact'
    StaticSlippage = 'static_slippage'


@unique
class ExecutionType(Enum):
    Close = 'Close'
    CloseAuctions = 'CloseAuctions'
    Open = 'Open'
    OpenAuctions = 'OpenAuctions'
    Vwap = 'Vwap'


@unique
class CostModelType(Enum):
    Equity = 'equity'
    Macro = 'macro'


@unique
class GicsLevel(Enum):
    Sector = 1
    Industry = 2
    Subindustry = 3
    
    
@unique
class SignalValueType(Enum):
    """
    Units/meaning for the VALUE field in an alpha.

    For bq is currently implemented for MoneyAllocation only.

    For bq-sim either MoneyAllocation or ExpectedReturns may be used.
    
    Money allocation means the target positions in US dollars.
    """
    MoneyAllocation = 'money_allocation'
    ExpectedReturns = 'expected_returns'
    Ranked = 'ranked'


@unique
class MissingHandlingType(Enum):
    Drift = 'drift'
    Error = 'error'
    Constant = 'constant'
    Zero = 'zero'
    Ignore = 'ignore'


@unique
class IntradayGMVOption(Enum):
    Max = 'max'
    EndOfDay = 'last'
    Mean = 'mean'


@unique
class FactorGroup(Enum):
    Style = 'Style'
    Industry = 'Industry'
    Market = 'Market'
    CustomFactor = 'Custom Factor'
    Country = 'Country'


# BQ_SIM
@unique
class FillType(Enum):
    Close = 'close'
    Vwap = 'vwap'


@unique
class OptimizerType(Enum):
    BAMOptimizer = 'bam_optimizer'
    Mosek = 'MOSEK'
    OSQP = 'OSQP'
    Blend = 'blend'


@unique
class DataLocationEnvironment(Enum):
    """
    Data location environment

    :param Enum: _description_
    :type Enum: _type_
    """
    Prod = 'prod'
    Dev = 'dev'
    Live = 'live'
    Test = 'test'

@unique
class RiskDataTimestamp(Enum):
    pos_t = 0
    pos_t_lag1 = 1
    pos_t_lag2 = 2
