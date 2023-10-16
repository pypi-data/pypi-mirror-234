import numpy as np
import pandas as pd
from enum import Enum


__all__ = [
    # true const
    'BEGINNING_DATE',
    'ACTIVE_DATE',
    'PrismComponentType',
    'SMValues',
    'CategoryComponent',
    'PACKAGE_NAME',
    'SPECIALVALUEMAP',
    'FILEEXTENSION',
    # param types
    'PreferenceType',
    'FrequencyType',
    'ScreenFrequencyType',
    'FBFrequencyType',
    'UniverseFrequencyType',
    'FinancialPeriodType',
    'EstimatePeriodType',
    'AdjustmentType',
    'DilutionType',
    'RankType',
    'DateType',
    'AggregationType',
    'FinancialPreliminaryType',
    'FillnaMethodType',
    'CompanyRelAttributeType',
]


BEGINNING_DATE = pd.to_datetime('1700-01-01')
ACTIVE_DATE = pd.to_datetime('2199-12-31')
SMValues = None
PreferenceType = None
CategoryComponent = None
FunctionComponents = None
TaskComponents = None
DataComponents = None


class PrismComponentType(str, Enum):
    FUNCTION_COMPONENT = 'functioncomponent'
    DATA_COMPONENT = 'datacomponent'
    TASK_COMPONENT = 'taskcomponent'
    MODEL_COMPONENT = 'modelcomponent'


class AdjustmentType(Enum):
    ALL = 'all'
    SPLIT = 'split'
    DIVIDEND = 'dividend'
    NONE = None

class CompanyRelAttributeType(Enum):
    COMPANYNAME = "companyname"
    LISTINGID = "listingid"
    COMPANYID = "companyid"


class DilutionType(Enum):
    ALL = "all"
    PARTNER = "partner"
    EXERCISABLE = "exercisable"


class FrequencyType(str, Enum):
    NANOSECONDS = 'N'
    MICROSECONDS = 'U'
    MICROSECONDS_ALIAS = 'us'
    MILISECONDS = 'L'
    MILISECONDS_ALIAS = 'ms'
    SECONDS = 'S'
    MINUTES = 'T'
    MINUTES_ALIAS = 'min'
    HOURS = 'H'
    BUSINESS_HOURS = 'BH'
    CALENDAR_DAY = 'D'
    BUSINESS_DAY = 'BD'
    WEEKS = 'W'
    MONTH_START = 'MS'
    BUSINESS_MONTH_START = 'BMS'
    SEMI_MONTH_START = 'SMS'
    SEMI_MONTH_END = 'SM'
    BUSINESS_MONTH_END = 'BM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    QUARTER_START = 'QS'
    BUSINESS_QUARTER_END = 'BQ'
    BUSINESS_QUARTER_START = 'BQS'
    YEAR_START = 'AS'
    YEAR_END = 'A'


class ResampleFrequencyType(str, Enum):
    CALENDAR_DAY = 'D'
    BUSINESS_DAY = 'BD'
    WEEKS = 'W'
    BUSINESS_MONTH_END = 'BM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    YEAR_END = 'A'


class ScreenFrequencyType(str, Enum):
    CALENDAR_DAY = 'D'
    BUSINESS_DAY = 'BD'
    WEEKS = 'W'
    BUSINESS_MONTH_END = 'BM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    YEAR_END = 'A'


class FBFrequencyType(str, Enum):
    CALENDAR_DAY = 'D'
    BUSINESS_DAY = 'BD'
    WEEKS = 'W'
    BUSINESS_MONTH_END = 'BM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    YEAR_END = 'A'


class UniverseFrequencyType(str, Enum):
    CALENDAR_DAY = 'D'
    WEEKS = 'W'
    MONTH_START = 'MS'
    SEMI_MONTH_START = 'SMS'
    SEMI_MONTH_END = 'SM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    QUARTER_START = 'QS'
    YEAR_START = 'AS'
    YEAR_END = 'A'


class RankType(str, Enum):
    STANDARD = 'standard'
    MODIFIED = 'modified'
    DENSE = 'dense'
    ORDINAL = 'ordinal'
    FRACTIONAL = 'fractional'


class DateType(str, Enum):
    ENTEREDDATE = 'entereddate'
    ANNOUNCEDDATE = 'announceddate'


class FinancialPeriodType(str, Enum):
    ANNUAL = 'Annual'
    A = 'A'
    SEMI_ANNUAL = 'Semi-Annual'
    SA = 'SA'
    QUARTERLY = 'Quarterly'
    Q = 'Q'
    YTD = 'YTD'
    LTM = 'LTM'
    QSA = 'Q-SA'


class EstimatePeriodType(str, Enum):
    ANNUAL = 'Annual'
    A = 'A'
    SEMI_ANNUAL = 'Semi-Annual'
    SA = 'SA'
    QUARTERLY = 'Quarterly'
    Q = 'Q'
    NTM = 'NTM'
    QSA = 'Q-SA'
    NONE = None


class AggregationType(str, Enum):
    ONEDAY = '1 day'
    ONEWEEK = '1 week'
    ONEMONTH = '1 month'
    TWOMONTH = '2 month'
    THREEMONTH = '3 month'
    THREEMONTHLATEST = '3 month latest'


class FinancialPreliminaryType(str, Enum):
    KEEP = 'keep'
    IGNORE = 'ignore'
    NULL = 'null'


class FillnaMethodType(str, Enum):
    BACKFILL = 'backfill'
    BFILL = 'bfill'
    PAD = 'pad'
    FFILL = 'ffill'
    NONE = None


FILEEXTENSION = {'pdq': 'dataquery', 'ptq': 'taskquery', 'pws': 'workspace', 'puv': 'universe', 'ppt': 'portfolio', 'ped': 'datafile'}


# PACKAGE_NAME = 'p3s9'
PACKAGE_NAME = 'prism'


SPECIALVALUEMAP = {
    np.nan: "\x01NaN",
    np.inf: "\x01inf",
    np.NINF: "\x01ninf",
}


DaysRepr = [
    'm',
    'mon',
    'monday',
    't',
    'tu',
    'tue',
    'tues',
    'tuesday',
    'w',
    'wed',
    'wednesday',
    'r',
    'th',
    'thu',
    'thurs',
    'thursday',
    'f',
    'fr',
    'fri',
    'friday',
    's',
    'sa',
    'sat',
    'saturday',
    'u',
    'su',
    'sun',
    'sunday'
]
