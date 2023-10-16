from typing import Union

import pandas as pd

from .._req_builder import _list_dataitem, _dataquery
from ..._common.const import AdjustmentType as _AdjustmentType, DilutionType as _DilutionType
from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from ..._utils import _get_params, _validate_args, _req_call


__all__ = [
    'open',
    'close',
    'high',
    'low',
    'bid',
    'ask',
    'vwap',
    'market_cap',
    'volume',
    'dividend',
    'exchange_rate',
    'short_interest',
    'split',
    'split_adjustment_factor',
    'dividend_adjustment_factor',
    'shares_outstanding',
    'enterprise_value',
    'implied_market_cap',
    'dataitems',
]


_data_category = __name__.split(".")[-1]


class _PrismMarketComponent(_PrismDataComponent, _PrismComponent):
    _component_category_repr = _data_category


class open(_PrismMarketComponent):
    """
    | Daily open pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily open prices for stocks

    Examples
    --------
        >>> open_prc = prism.market.open(adjustment='all', package='Prism Market')
        >>> open_df = prism.get_data([open_prc], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> open_df
                listingid        date           Open   ticker
        0        20108718  2015-01-02    7711.942343  A004430
        1        20108718  2015-01-05    7625.935551  A004430
        2        20108718  2015-01-06    7750.167583  A004430
        3        20108718  2015-01-07    7845.730686  A004430
        4        20108718  2015-01-08    8342.658817  A004430
        ...           ...         ...            ...      ...
        298991  686744025  2020-12-23  152679.990000  A352820
        298992  686744025  2020-12-24  151197.660000  A352820
        298993  686744025  2020-12-28  156632.870000  A352820
        298994  686744025  2020-12-29  154656.430000  A352820
        298995  686744025  2020-12-30  156632.870000  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class close(_PrismMarketComponent):
    """
    | Daily close pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily close prices for stocks

    Examples
    --------
        Obtain daily closing prices for a specific security:

        >>> close = prism.market.close(adjustment='all', package='Prism Market')
        >>> close_df = prism.get_data([close], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> close_df
                listingid        date          Close   ticker
        0        20108718  2015-01-02    7740.611273  A004430
        1        20108718  2015-01-05    7874.399616  A004430
        2        20108718  2015-01-06    7903.068547  A004430
        3        20108718  2015-01-07    8313.989886  A004430
        4        20108718  2015-01-08    8161.088923  A004430
        ...           ...         ...            ...      ...
        298992  686744025  2020-12-23  151197.660000  A352820
        298993  686744025  2020-12-24  156138.760000  A352820
        298994  686744025  2020-12-28  154656.430000  A352820
        298995  686744025  2020-12-29  156632.870000  A352820
        298996  686744025  2020-12-30  158115.200000  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class high(_PrismMarketComponent):
    """
    | Daily high pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all: apply both split and dividend adjustment
            - split: apply only split adjustment
            - dividend: apply only dividend adjustment

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily high prices for stocks

    Examples
    --------
        >>> high = prism.market.high(adjustment='all', package='Prism Market')
        >>> high_df = prism.get_data([high], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> high_df
                listingid        date           High   ticker
        0        20108718  2015-01-02    7855.286996  A004430
        1        20108718  2015-01-05    7893.512237  A004430
        2        20108718  2015-01-06    7931.737478  A004430
        3        20108718  2015-01-07    8323.546196  A004430
        4        20108718  2015-01-08    8352.215127  A004430
        ...           ...         ...            ...      ...
        298991  686744025  2020-12-23  156138.760000  A352820
        298992  686744025  2020-12-24  156632.870000  A352820
        298993  686744025  2020-12-28  157126.980000  A352820
        298994  686744025  2020-12-29  158609.310000  A352820
        298995  686744025  2020-12-30  159103.420000  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class low(_PrismMarketComponent):
    """
    | Daily low pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily low prices for stocks

    Examples
    --------
        >>> low = prism.market.low(adjustment='all', package='Prism Market')
        >>> low_df = prism.get_data([low], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> low_df
                listingid       date            Low   ticker
        0        20108718 2015-01-02    7501.703518  A004430
        1        20108718 2015-01-05    7539.928759  A004430
        2        20108718 2015-01-06    7750.167583  A004430
        3        20108718 2015-01-07    7836.174375  A004430
        4        20108718 2015-01-08    8141.976302  A004430
        ...           ...        ...            ...      ...
        298991  686744025 2020-12-23  150703.550000  A352820
        298992  686744025 2020-12-24  149715.330000  A352820
        298993  686744025 2020-12-28  153174.100000  A352820
        298994  686744025 2020-12-29  153174.100000  A352820
        298995  686744025 2020-12-30  155644.650000  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class ask(_PrismMarketComponent):
    """
    | End of day ask pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'Prism Market', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily end of day ask prices for stocks

    Examples
    --------
        >>> ask = prism.market.ask(adjustment='all', package='Prism Market')
        >>> ask_df = prism.get_data([ask], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> ask_df
                listingid        date            Ask   ticker
        0        20108718  2015-01-02    7740.611273  A004430
        1        20108718  2015-01-05    7874.399616  A004430
        2        20108718  2015-01-06    7903.068547  A004430
        3        20108718  2015-01-07    8313.989886  A004430
        4        20108718  2015-01-08    8199.314164  A004430
        ...           ...         ...            ...      ...
        298906  686744025  2020-12-23  151691.770000  A352820
        298907  686744025  2020-12-24  156138.760000  A352820
        298908  686744025  2020-12-28  155150.540000  A352820
        298909  686744025  2020-12-29  157126.980000  A352820
        298910  686744025  2020-12-30  158115.200000  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class bid(_PrismMarketComponent):
    """
    | End of day bid pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend: apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'Prism Market', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily end of day ask prices for stocks

    Examples
    --------
        >>> bid = prism.market.bid(adjustment='all', package='Prism Market')
        >>> bid_df = prism.get_data([bid], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> bid_df
                listingid        date            Bid   ticker
        0        20108718  2015-01-02    7616.379240  A004430
        1        20108718  2015-01-05    7864.843306  A004430
        2        20108718  2015-01-06    7883.955926  A004430
        3        20108718  2015-01-07    8304.433576  A004430
        4        20108718  2015-01-08    8161.088923  A004430
        ...           ...         ...            ...      ...
        298976  686744025  2020-12-23  151197.660000  A352820
        298977  686744025  2020-12-24  155644.650000  A352820
        298978  686744025  2020-12-28  154656.430000  A352820
        298979  686744025  2020-12-29  156632.870000  A352820
        298980  686744025  2020-12-30  157621.090000  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class vwap(_PrismMarketComponent):
    """
    | Daily VWAP pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'CIQ Market'}, default 'CIQ Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> vwap = prism.market.ask(adjustment='all', package='CIQ Market')
        >>> vwap_df = prism.get_data([vwap], 'KOSPI 200 Index', startdate='2019-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> vwap_df
               listingid        date          VWAP   ticker
        0       20113302  2019-01-02  44884.613444  A078930
        1       20113302  2019-01-03  44146.922268  A078930
        2       20113302  2019-01-04  44883.697058  A078930
        3       20113302  2019-01-07  45929.294117  A078930
        4       20113302  2019-01-08  45773.508402  A078930
        ...          ...         ...           ...      ...
        97551  643903265  2020-12-23  14429.849563  A272210
        97552  643903265  2020-12-24  15179.657143  A272210
        97553  643903265  2020-12-28  16643.755102  A272210
        97554  643903265  2020-12-29  17252.000000  A272210
        97555  643903265  2020-12-30  17067.000000  A272210
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class market_cap(_PrismMarketComponent):
    """
    | Market capitalization history for equity securities aggregated to the company level.
    | Default frequency is daily.

    Parameters
    ----------

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'CIQ Market'}, default 'CIQ Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.


    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> mcap = prism.market.market_cap()
        >>> mcap_df = mcap.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> mcap_df
                listingid        date     marketcap   Ticker
        0        20108718  2010-06-11  2.592000e+11  A004430
        1        20108718  2010-06-12  2.592000e+11  A004430
        2        20108718  2010-06-13  2.592000e+11  A004430
        3        20108718  2010-06-14  2.592000e+11  A004430
        4        20108718  2010-06-15  2.640000e+11  A004430
        ...           ...         ...           ...      ...
        437100  278631846  2015-12-27  2.433650e+13  A028260
        437101  278631846  2015-12-28  2.317036e+13  A028260
        437102  278631846  2015-12-29  2.375490e+13  A028260
        437103  278631846  2015-12-30  2.341962e+13  A028260
        437104  278631846  2015-12-31  2.341962e+13  A028260
    """
    @_validate_args
    def __init__(
        self,
        currency: str = 'trade',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class volume(_PrismMarketComponent):
    """
    | Daily volume for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment

        package : str, {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> volume = prism.market.volume(package='MI Integrated Market')
        >>> volume_df = prism.get_data([volume], 'KOSPI 200 Index', startdate='2019-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> volume_df
                listingid        date    volume   ticker
        0        20113302  2019-01-02  271000.0  A078930
        1        20113302  2019-01-03  178985.0  A078930
        2        20113302  2019-01-04  166248.0  A078930
        3        20113302  2019-01-07  118530.0  A078930
        4        20113302  2019-01-08  112217.0  A078930
        ...           ...         ...       ...      ...
        100638  686744025  2020-12-23  149780.0  A352820
        100639  686744025  2020-12-24  132606.0  A352820
        100640  686744025  2020-12-28  115532.0  A352820
        100641  686744025  2020-12-29  110664.0  A352820
        100642  686744025  2020-12-30  117489.0  A352820
    """
    @_validate_args
    def __init__(
        self,
        adjustment: _AdjustmentType = 'all',
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class dividend(_PrismMarketComponent):
    """
    | Dividend history for equity securities.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        adjustment : bool, default True
            | Whether to apply split adjustment for dividend data.

        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
            - None : dividend payment currency

        aggregate: bool, default True
            | Desired aggregation for dividend. If True, dividends are aggregated based on listingid and exdate.

            - If `True`, paymentdate and dividendtype column will be dropped
            - If `True`, and currency is `None`, the currency will be automatically set to `trade`

        package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> dividend = prism.market.dividend(package='MI Integrated Market')
        >>> dividend _df = prism.get_data([dividend], 'KOSPI 200 Index', startdate='2019-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> dividend _df
              listingid        date  dividend  Ticker
        0       2586086  2010-02-11      0.14     AFL
        1       2586086  2010-05-17      0.14     AFL
        2       2586086  2010-08-16      0.14     AFL
        3       2586086  2010-11-15      0.15     AFL
        4       2586086  2011-02-11      0.15     AFL
                    ...         ...       ...     ...
        9544  344286611  2010-08-25      0.50     ITT
        9545  344286611  2010-11-09      0.50     ITT
        9546  344286611  2011-02-28      0.50     ITT
        9547  344286611  2011-05-18      0.50     ITT
        9548  344286611  2011-08-24      0.50     ITT
    """
    @_validate_args
    def __init__(
        self,
        adjustment: bool = True,
        currency: str = 'trade',
        aggregate: bool = True,
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class dividend_adjustment_factor(_PrismMarketComponent):
    """
    | Dividend adjustment factor history for equity securities.
    | Default frequency is daily.

    Parameters
    ----------
    package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
        | Desired data package in where the pricing data outputs from.

        .. admonition:: Warning
            :class: warning

            If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> divadj = prism.market.dividend_adjustment_factor()
        >>> divadj_df = divadj.get_data()
    """
    @_validate_args
    def __init__(self, package : str = None):
        super().__init__(**_get_params(vars()))


class split(_PrismMarketComponent):
    """
    | Return the split history for equity securities.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
    package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
        | Desired data package in where the pricing data outputs from.

        .. admonition:: Warning
            :class: warning

            If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> split = prism.market.split()
        >>> split_df = split.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> split_df
            listingid        date     split   Ticker
        0    20126254  2015-07-29  1.350000  A014830
        1    20158335  2013-04-30  0.100000  A008000
        2    20158445  2015-01-01  0.620935  A004150
        3    20158447  2010-12-29  1.030000  A001060
        4    20158758  2012-10-19  0.142857  A001440
        ..        ...         ...       ...      ...
        60  104646533  2014-09-01  0.478239  A060980
        61  107478344  2012-12-27  1.050000  A128940
        62  107478344  2014-02-10  1.050000  A128940
        63  107478344  2014-12-29  1.050000  A128940
        64  107478344  2015-12-29  1.020000  A128940
    """
    @_validate_args
    def __init__(self, package : str = None):
        super().__init__(**_get_params(vars()))


class split_adjustment_factor(_PrismMarketComponent):
    """
    | Split adjustment factor history for equity securities.
    | Default frequency is daily.

    Parameters
    ----------
    package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
        | Desired data package in where the pricing data outputs from.

        .. admonition:: Warning
            :class: warning

            If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent
    """
    @_validate_args
    def __init__(self, package : str = None):
        super().__init__(**_get_params(vars()))


class exchange_rate(_PrismMarketComponent):
    """
    | Daily exchange rate history.
    | Default frequency is daily.

    Parameters
    ----------
        currency : list of ISO3 currency
            | Desired exchange rates.
        to_convert : bool, default False
            | True
            | False : business daily
        package : str, {'Compustat', 'CIQ Market'}, default 'CIQ Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> exrt = prism.market.exchange_rate(currency=['USD', 'KRW'])
        >>> exrt_df = exrt.get_data(startdate='2010-01-01', enddate='2015-12-31')
        >>> exrt_df
            currency        date       exrt
        0         KRW  2010-01-01  1881.5000
        1         KRW  2010-01-02  1881.5000
        2         KRW  2010-01-03  1881.5000
        3         KRW  2010-01-04  1854.5000
        4         KRW  2010-01-05  1826.1000
        ...       ...         ...        ...
        3873      USD  2015-12-27     1.4933
        3874      USD  2015-12-28     1.4903
        3875      USD  2015-12-29     1.4795
        3876      USD  2015-12-30     1.4833
        3877      USD  2015-12-31     1.4740
    """
    @_validate_args
    def __init__(self, currency: list, to_convert: bool = False, package : str = None):
        super().__init__(**_get_params(vars()))

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, name = None,) -> pd.DataFrame: ...


class short_interest(_PrismMarketComponent):
    """
    | Short interest dataitems for equity securities and global data coverage.
    | Default frequency is business daily.

    Parameters
    ----------
    dataitemid : int
        | Unique identifier for the different dataitem. This identifies the type of the value (Revenue, Expense, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> prism.market.short_interest.dataitems(search='short')
           dataitemid                               dataitemname  ...  datamodule                packagename
        0     1100035                Broker Short Interest Value  ...        None  IHS Markit Short Interest
        1     1100055        Short Interest Ratio (Day to Cover)  ...        None  IHS Markit Short Interest
        2     1100056                      Short Interest Tenure  ...        None  IHS Markit Short Interest
        3     1100057                       Short Interest Value  ...        None  IHS Markit Short Interest
        4     1100058          Short Interest as % Of Free Float  ...        None  IHS Markit Short Interest
        5     1100059  Short Interest as % Of Shares Outstanding  ...        None  IHS Markit Short Interest
        6     1100060                                Short Score  ...        None  IHS Markit Short Interest
        7     1100063           Supply Side Short Interest Value  ...        None  IHS Markit Short Interest

        >>> short = prism.market.short_interest(dataitemid=1100057)
        >>> short_df = short.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> short_df
                listingid        date  shortinterestvalue   Ticker
        0        20108718  2010-06-11        1.288440e+08  A004430
        1        20108718  2010-06-14        1.288440e+08  A004430
        2        20108718  2010-06-15        1.298000e+08  A004430
        3        20108718  2010-06-16        1.309800e+08  A004430
        4        20108718  2010-06-17        6.660000e+07  A004430
        ...           ...         ...                 ...      ...
        305527  278631846  2015-12-25        7.331920e+10  A028260
        305528  278631846  2015-12-28        7.045744e+10  A028260
        305529  278631846  2015-12-29        7.223796e+10  A028260
        305530  278631846  2015-12-30        6.464626e+10  A028260
        305531  278631846  2015-12-31        6.800626e+10  A028260
    """
    @_validate_args
    def __init__(self, dataitemid: int, currency: str = 'trade', package : str = None):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search : str = None, package : str = None):
        """
        | Usable data items for the short_interest data component.

        Parameters
        ----------
            search : str, default None
                | Search word for data items name, the search is case-insensitive.
            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                Data items that belong to short_interest data component.

            Columns:
                - *dataitemid : int*
                - *dataitemname : str*
                - *dataitemdescription : str*
                - *datamodule : str*
                - *datacomponent : str*
                - *packagename : str*

        Examples
        --------
            >>> prism.market.short_interest.dataitems(search='short')
            dataitemid                                  dataitemname  ...  datamodule                packagename
            0     1100035                Broker Short Interest Value  ...        None  IHS Markit Short Interest
            1     1100055        Short Interest Ratio (Day to Cover)  ...        None  IHS Markit Short Interest
            2     1100056                      Short Interest Tenure  ...        None  IHS Markit Short Interest
            3     1100057                       Short Interest Value  ...        None  IHS Markit Short Interest
            4     1100058          Short Interest as % Of Free Float  ...        None  IHS Markit Short Interest
            5     1100059  Short Interest as % Of Shares Outstanding  ...        None  IHS Markit Short Interest
            6     1100060                                Short Score  ...        None  IHS Markit Short Interest
            7     1100063           Supply Side Short Interest Value  ...        None  IHS Markit Short Interest
        """
        return _list_dataitem(
            datacategoryid=cls.categoryid,
            datacomponentid=cls.componentid,
            search=search,
            package=package,
        )


class shares_outstanding(_PrismMarketComponent):
    """
    | The total number of shares of a security that are currently held by all its shareholders and are available for trading on a specific stock exchange.
    | Default frequency is daily.

    Parameters
    ----------
    adjustment : bool, default True
        | Adjustment for Shares outstanding

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> shares_out = prism.market.shares_outstanding()
        >>> shares_out.get_data("Semiconductor", "2020-01-01", shownid=['Company Name'])
                  listingid        date      shares                                       Company Name
        0           2586491  2020-01-01    39521782                                          AXT, Inc.
        1           2587243  2020-01-01    22740986                                  Aehr Test Systems
        2           2587303  2020-01-01  1138599272                       Advanced Micro Devices, Inc.
        3           2587347  2020-01-01    38308569                   Advanced Energy Industries, Inc.
        4           2589783  2020-01-01   239783075                             Amkor Technology, Inc.
        ...             ...         ...         ...                                                ...
        1168126  1831385562  2023-07-26     7501500                                        SEALSQ Corp
        1168127  1833187092  2023-07-26    12675758                                  GigaVis Co., Ltd.
        1168128  1833609849  2023-07-26  7021800000  Semiconductor Manufacturing Electronics (Shaox...
        1168129  1834641950  2023-07-26   452506348     Smarter Microelectronics (Guangzhou) Co., Ltd.
        1168130  1838168164  2023-07-26    37844925              Integrated Solutions Technology, Inc.
    """
    @_validate_args
    def __init__(self, adjustment: bool = True, package : str = None):
        super().__init__(**_get_params(vars()))


class enterprise_value(_PrismMarketComponent):
    """
    | Represents the total value of a company, taking into account its market capitalization, outstanding debt, cash, and other financial assets.
    | It is used to determine the true cost of acquiring a company and is calculated as market capitalization plus total debt minus cash and cash equivalents.
    | Default frequency is daily.

    Parameters
    ----------
    currency : str, {'trade', 'report', ISO3 currency}, default None
            | Desired currency for the enterprise value data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
            - None : dividend payment currency

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> ent_val = prism.market.enterprise_value(currency='trade')
        >>> ent_val.get_data("Semi", "2020-01-01", shownid=['Company Name'])
                  listingid        date           tev  currency                                       Company Name
        0           2586491  2020-01-01  1.546798e+08       USD                                          AXT, Inc.
        1           2587243  2020-01-01  4.288797e+07       USD                                  Aehr Test Systems
        2           2587303  2020-01-01  5.211816e+10       USD                       Advanced Micro Devices, Inc.
        3           2587347  2020-01-01  2.842980e+09       USD                   Advanced Energy Industries, Inc.
        4           2589783  2020-01-01  3.988825e+09       USD                             Amkor Technology, Inc.
        ...             ...         ...           ...       ...                                                ...
        1167719  1831385562  2023-07-25  1.645610e+08       USD                                        SEALSQ Corp
        1167720  1833187092  2023-07-25           NaN       KRW                                  GigaVis Co., Ltd.
        1167721  1833609849  2023-07-25  5.481000e+10       CNY  Semiconductor Manufacturing Electronics (Shaox...
        1167722  1834641950  2023-07-25  9.114210e+09       CNY     Smarter Microelectronics (Guangzhou) Co., Ltd.
        1167723  1838168164  2023-07-25           NaN       TWD              Integrated Solutions Technology, Inc.
    """
    @_validate_args
    def __init__(self, currency: str = None, package : str = None):
        super().__init__(**_get_params(vars()))


class implied_market_cap(_PrismMarketComponent):
    """
    | Theoretical total value of a company's outstanding shares, including potential dilution from stock options and other equity-based compensation plans.
    | Default frequency is daily.

    Parameters
    ----------
    dilution : str, {'all', 'partner', 'exercisable'}, default 'all'
            | Options whether to include which potential dilution from stock options and other equity-based compensation plans.

    currency : str, {'trade', 'report', ISO3 currency}, default None
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
            - None : dividend payment currency

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> immcap = prism.market.implied_market_cap()
        >>> immcap.get_data("Semi", "2020-01-01", shownid=['Company Name'])
             listingid        date    implieddilutedmarketcapout  currency               Company Name
        0    707934944  2021-06-24                  1.317918e+09       USD  indie Semiconductor, Inc.
        1    707934944  2021-06-25                  1.335508e+09       USD  indie Semiconductor, Inc.
        2    707934944  2021-06-26                  1.335508e+09       USD  indie Semiconductor, Inc.
        3    707934944  2021-06-27                  1.335508e+09       USD  indie Semiconductor, Inc.
        4    707934944  2021-06-28                  1.332802e+09       USD  indie Semiconductor, Inc.
        ...        ...         ...                           ...       ...                        ...
        762  707934944  2023-07-26                  1.485848e+09       USD  indie Semiconductor, Inc.
        763  707934944  2023-07-27                  1.464184e+09       USD  indie Semiconductor, Inc.
        764  707934944  2023-07-28                  1.502095e+09       USD  indie Semiconductor, Inc.
        765  707934944  2023-07-29                  1.502095e+09       USD  indie Semiconductor, Inc.
        766  707934944  2023-07-30                  1.502095e+09       USD  indie Semiconductor, Inc.


    """
    @_validate_args
    def __init__(self, dilution: _DilutionType = 'all', currency: str = None, package : str = None):
        super().__init__(**_get_params(vars()))


@_validate_args
def dataitems(search : str = None, package : str = None):
    """
    | Usable dataitems for the market data categories.

    Parameters
    ----------
        search : str, default None
            | Search word for Data Items name, the search is case-insensitive.
        package : str, default None
            | Search word for package name, the search is case-insensitive.

    Returns
    -------
        pandas.DataFrame
            Data items that belong to market data categories.

        Columns:
            - *dataitemid : int*
            - *dataitemname : str*
            - *dataitemdescription : str*
            - *datamodule : str*
            - *datacomponent : str*
            - *packagename : str*

    Examples
    --------
        >>> prism.market.dataitems(search='short')
            dataitemid                               dataitemname  ...   datacomponent                packagename
        0     1100035                Broker Short Interest Value  ...  Short Interest  IHS Markit Short Interest
        1     1100055        Short Interest Ratio (Day to Cover)  ...  Short Interest  IHS Markit Short Interest
        2     1100056                      Short Interest Tenure  ...  Short Interest  IHS Markit Short Interest
        3     1100057                       Short Interest Value  ...  Short Interest  IHS Markit Short Interest
        4     1100058          Short Interest as % Of Free Float  ...  Short Interest  IHS Markit Short Interest
        5     1100059  Short Interest as % Of Shares Outstanding  ...  Short Interest  IHS Markit Short Interest
        6     1100060                                Short Score  ...  Short Interest  IHS Markit Short Interest
        7     1100063           Supply Side Short Interest Value  ...  Short Interest  IHS Markit Short Interest
    """
    return _list_dataitem(
        datacategory=_PrismMarketComponent.categoryid,
        datacomponent=None,
        search=search,
        package=package,
    )
