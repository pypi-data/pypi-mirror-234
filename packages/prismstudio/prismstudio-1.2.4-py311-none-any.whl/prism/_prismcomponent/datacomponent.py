import pandas as pd

from .._common.const import (
    EstimateDataComponentType,
    FinancialDataComponentType,
    MarketDataComponentType,
    PrecalculatedDataComponentType,
    IndexDataComponentType,
    EventDataComponentType,
    OtherDataComponentType,
    IndustryComponentType,
    DataCategoryType,
    ESGDataComponentType
)
from .._core._req_builder import _dataquery
from .._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent, _PrismFinancialComponent
from .._utils import _validate_args, _req_call


# ------------------------------------------------------------------------------------------------------------------- #
#                                                        Market                                                       #
# ------------------------------------------------------------------------------------------------------------------- #
class _PrismMarketComponent(_PrismDataComponent, _PrismComponent):
    _component_category = DataCategoryType.MARKET


class _Open(_PrismMarketComponent):
    _component_name = MarketDataComponentType.OPEN


class _Close(_PrismMarketComponent):
    _component_name = MarketDataComponentType.CLOSE


class _High(_PrismMarketComponent):
    _component_name = MarketDataComponentType.HIGH


class _Low(_PrismMarketComponent):
    _component_name = MarketDataComponentType.LOW


class _Bid(_PrismMarketComponent):
    _component_name = MarketDataComponentType.BID


class _Ask(_PrismMarketComponent):
    _component_name = MarketDataComponentType.ASK


class _VWAP(_PrismMarketComponent):
    _component_name = MarketDataComponentType.VWAP


class _MarketCap(_PrismMarketComponent):
    _component_name = MarketDataComponentType.MARKETCAP


class _Volume(_PrismMarketComponent):
    _component_name = MarketDataComponentType.VOLUME


class _ShortInterest(_PrismMarketComponent):
    _component_name = MarketDataComponentType.SHORT_INTEREST


class _Dividend(_PrismMarketComponent):
    _component_name = MarketDataComponentType.DIVIDEND


class _DividendAdjustmentFactor(_PrismMarketComponent):
    _component_name = MarketDataComponentType.DIVIDEND_ADJ_FACTOR


class _Split(_PrismMarketComponent):
    _component_name = MarketDataComponentType.SPLIT


class _SplitAdjustmentFactor(_PrismMarketComponent):
    _component_name = MarketDataComponentType.SPLIT_ADJ_FACTOR


class _ExchangeRate(_PrismMarketComponent):
    _component_name = MarketDataComponentType.EXCHANGERATE

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, name = None,) -> pd.DataFrame:
        pass


class _SharesOutstanding(_PrismMarketComponent):
    _component_name = MarketDataComponentType.SHARES_OUTSTANDING


class _TotalEnterpriseValue(_PrismMarketComponent):
    _component_name = MarketDataComponentType.TOTAL_ENTERPRISE_VALUE


class _ImpliedMarketCapitalization(_PrismMarketComponent):
    _component_name = MarketDataComponentType.IMPLIED_MARKET_CAPITALIZATION


# ------------------------------------------------------------------------------------------------------------------- #
#                                                      Financial                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _BalanceSheet(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.BALANCE_SHEET


class _IncomeStatement(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.INCOME_STATEMENT


class _DPS(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.DPS


class _EPS(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.EPS


class _CashFlow(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.CASH_FLOW


class _FinancialDate(_PrismDataComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.FINANCIAL_DATE


class _Segment(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.SEGMENT


class _Ratio(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.RATIO


class _Commitment(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.COMMITMENT


class _Pension(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.PENSION


class _Option(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.FINANCIAL
    _component_name = FinancialDataComponentType.OPTION


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       Estimate                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _PrismEstimateComponent(_PrismDataComponent, _PrismComponent):
    _component_category = DataCategoryType.ESTIMATE


class _Consensus(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.CONSENSUS


class _Growth(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.GROWTH


class _Guidance(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.GUIDANCE


class _Revision(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.REVISION


class _Actual(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.ACTUAL


class _Surprise(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.SURPRISE


class _Recommendation(_PrismEstimateComponent):
    _component_name = EstimateDataComponentType.RECOMMENDATION


# ------------------------------------------------------------------------------------------------------------------- #
#                                                          SM                                                         #
# ------------------------------------------------------------------------------------------------------------------- #
class _SecurityMasterAttribute(_PrismDataComponent, _PrismComponent):
    _component_category = DataCategoryType.SM
    _component_name = OtherDataComponentType.SM


# ------------------------------------------------------------------------------------------------------------------- #
#                                                    Precalculated                                                    #
# ------------------------------------------------------------------------------------------------------------------- #
class _AFL(_PrismDataComponent, _PrismComponent):
    _component_category = DataCategoryType.PRECALCAULATED
    _component_name = PrecalculatedDataComponentType.AFL


# ------------------------------------------------------------------------------------------------------------------- #
#                                                        Index                                                        #
# ------------------------------------------------------------------------------------------------------------------- #
class _PrismIndexComponent(_PrismDataComponent, _PrismComponent):
    _component_category = DataCategoryType.INDEX

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, shownid = None, name = None,) -> pd.DataFrame:
        pass


class _IndexShare(_PrismIndexComponent):
    _component_name = IndexDataComponentType.SHARE


class _IndexWeight(_PrismIndexComponent):
    _component_name = IndexDataComponentType.WEIGHT


class _IndexLevel(_PrismIndexComponent):
    _component_name = IndexDataComponentType.LEVEL

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, name = None,) -> pd.DataFrame:
        pass


# ------------------------------------------------------------------------------------------------------------------- #
#                                                        Event                                                        #
# ------------------------------------------------------------------------------------------------------------------- #
class _News(_PrismDataComponent):
    _component_category = DataCategoryType.PRECALCAULATED
    _component_name = EventDataComponentType.NEWS


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       Industry                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _PrismIndustryFinancialComponent(_PrismDataComponent, _PrismFinancialComponent):
    _component_category = DataCategoryType.INDUSTRY_FINANCIAL


class _Airlines(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.AIRLINES


class _Bank(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.BANK


class _CapitalMarket(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.CAPITAL_MARKET


class _FinancialServices(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.FINAICIAL_SERVICES


class _Healthcare(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.HEALTHCARE


class _Homebuilders(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.HOMBUILDERS


class _HotelandGaming(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.HOTEL_AND_GAMING


class _Insurance(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.INSURANCE


class _InternetMedia(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.INTERNET_MEDIA


class _ManagedCare(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.MANAGED_CARE


class _MetalsandMining(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.METALS_AND_MINING


class _OilandGas(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.OIL_AND_GAS


class _Pharmaceutical(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.PHARMA


class _RealEstate(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.REAL_ESTATE


class _Restaurant(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.RESTAURANT


class _Retail(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.RETAIL


class _Semiconductors(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.SEMICONDUCTORS


class _Telecom(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.TELECOM


class _Utility(_PrismIndustryFinancialComponent):
    _component_name = IndustryComponentType.UTILITY


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       ESG                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _PrismESGComponent(_PrismDataComponent, _PrismComponent):
    _component_category = DataCategoryType.ESG
    # @_validate_args
    # @_req_call(_dataquery)
    # def get_data(self, startdate: str = None, enddate: str = None, name = None,) -> pd.DataFrame:
    #     pass


class _Environmental(_PrismESGComponent):
    _component_name = ESGDataComponentType.ENVIRONMENTAL


class _Social(_PrismESGComponent):
    _component_name = ESGDataComponentType.SOCIAL


class _Governance(_PrismESGComponent):
    _component_name = ESGDataComponentType.GOVERNANCE


class _Summary(_PrismESGComponent):
    _component_name = ESGDataComponentType.SUMMARY
