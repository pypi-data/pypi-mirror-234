from prism._utils.exceptions import PrismValueError
from ..._common.const import (
    AggregationType as _AggregationType,
    EstimatePeriodType as _PeriodType,
)
from .._req_builder import _list_dataitem
from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from ..._utils import _validate_args, _get_params


__all__ = [
    'actual',
    'consensus',
    'growth',
    'guidance',
    'recommendation',
    'revision',
    'surprise',
    'dataitems',
]


_data_category = __name__.split(".")[-1]


class _PrismEstimateComponent(_PrismDataComponent, _PrismComponent):
    _component_category_repr = _data_category

    def __init__(self, **kwargs):
        if (kwargs.get('periodtype') == 'NTM') & (kwargs.get('periodout') != 0):
            raise PrismValueError("NTM period type only takes 0 periodout.")
        super().__init__(**kwargs)

    @classmethod
    def _dataitems(cls, search: str = None, package: str = None):
        return _list_dataitem(
            datacategoryid=cls.categoryid,
            datacomponentid=cls.componentid,
            search=search,
            package=package,
        )


class actual(_PrismEstimateComponent):
    """
    | Actual financial statement result that can be compared to the consensus estimate data for a data item.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)
        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the pricing data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.estimate.actual.dataitems('revenue')
        >>> di[['dataitemid', 'dataitemname']]
           dataitemid      dataitemname
        0      200032  Revenue - Actual

        >>> rev = prism.estimate.actual(dataitemid=200032, periodtype='Q')
        >>> rev_df = rev.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> rev_df
               listingid                 date  Revenue - Actual Ticker
        0        2611056  2010-01-06 12:00:00          1822.906    FDO
        1        2631428  2010-01-06 13:01:56          1697.000    MON
        2        2626233  2010-01-07 11:00:00           913.741    LEN
        3        2602822  2010-01-07 12:30:35           987.700    STZ
        4        2590296  2010-01-07 21:01:00          1270.301   APOL
                     ...                  ...               ...    ...
        10146    2598323  2015-12-18 14:15:00          3711.000    CCL
        10147    2600608  2015-12-21 21:15:00          1219.080   CTAS
        10148    2602239  2015-12-22 12:30:00          3092.700    CAG
        10149    2638038  2015-12-22 13:30:00           722.400   PAYX
        10150    2634146  2015-12-22 21:15:00          7686.000    NKE
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        currency: str = "report",
        package : str = None,
    ):
        if periodtype in ["NTM", None]:
            raise PrismValueError(
                f"Actual cannot take {periodtype} as periodtype.",
                valid_list=_PeriodType,
                invalids=["NTM", "None"],
            )
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable dataitems for the actual datacomponent.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> di = prism.estimate.actual.dataitems('net income')
            >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
            0      200027  Net Income (Excl. Extraordinary Items & Good W...
            1      200028                         Net Income (GAAP) - Actual
            2      200029                     Net Income Normalized - Actual
        """
        return cls._dataitems(search=search, package=package)


class consensus(_PrismEstimateComponent):
    """
    | Consensus estimate data item.
    | Default frequency is aperiodic.


    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

        periodout : int
            | Determines how far out estimate to fetch.
            | For example, inputting 0 will fetch estimate data for the current period, 1 will fetch estimate for the next period.

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the pricing data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)


    Returns
    -------
        prism._PrismComponent


    Examples
    --------
        >>> di = prism.estimate.consensus.dataitems('eps')
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       200047               Cash EPS - Consensus, # of Estimates
        1       200048                         Cash EPS - Consensus, High
        2       200049                          Cash EPS - Consensus, Low
        3       200050                         Cash EPS - Consensus, Mean
        4       200051                       Cash EPS - Consensus, Median
        5       200052           Cash EPS - Consensus, Standard Deviation
        6       200119  EPS (Excl. Extraordinary Items & Good Will) - ...
        7       200120  EPS (Excl. Extraordinary Items & Good Will) - ...
        8       200121  EPS (Excl. Extraordinary Items & Good Will) - ...
        9       200122  EPS (Excl. Extraordinary Items & Good Will) - ...
        10      200123  EPS (Excl. Extraordinary Items & Good Will) - ...
        11      200124  EPS (Excl. Extraordinary Items & Good Will) - ...
        12      200125             EPS (GAAP) - Consensus, # of Estimates
        13      200126                       EPS (GAAP) - Consensus, High
        14      200127                        EPS (GAAP) - Consensus, Low
        15      200128                       EPS (GAAP) - Consensus, Mean
        16      200129                     EPS (GAAP) - Consensus, Median
        17      200130         EPS (GAAP) - Consensus, Standard Deviation
        18      200131  EPS Long-Term Growth (%) - Consensus, # of Est...
        19      200132         EPS Long-Term Growth (%) - Consensus, High
        20      200133          EPS Long-Term Growth (%) - Consensus, Low
        21      200134         EPS Long-Term Growth (%) - Consensus, Mean
        22      200135       EPS Long-Term Growth (%) - Consensus, Median
        23      200136  EPS Long-Term Growth (%) - Consensus, Standard...
        24      200137         EPS Normalized - Consensus, # of Estimates
        25      200138                   EPS Normalized - Consensus, High
        26      200139                    EPS Normalized - Consensus, Low
        27      200140                   EPS Normalized - Consensus, Mean
        28      200141                 EPS Normalized - Consensus, Median
        29      200142     EPS Normalized - Consensus, Standard Deviation

        >>> eps = prism.estimate.consensus(dataitemid=200140, periodtype='Q')
        >>> eps_df = eps.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> eps_df
              listingid                 date  EPS Normalized - Consensus, Mean   Ticker
        0      20108958  2010-01-26 01:37:00                         8588.6960  A077970
        1      20108958  2011-08-29 11:56:36                         -776.0000  A077970
        2      20108958  2012-04-02 11:30:54                         2320.0000  A077970
        3      20108958  2012-08-29 01:17:12                         1200.0000  A077970
        4      20113302  2010-01-11 23:22:00                          922.0000  A078930
        ...         ...                  ...                               ...      ...
        8125  278631846  2015-04-09 00:30:47                          423.0076  A028260
        8126  278631846  2015-04-29 10:53:38                          243.5500  A028260
        8127  278631846  2015-04-29 13:30:47                          369.1384  A028260
        8128  278631846  2015-10-21 09:36:10                        14533.4700  A028260
        8129  278631846  2015-11-04 12:51:57                          497.4083  A028260
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType = None,
        periodout: int = 0,
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the estimate consensus data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*


        Examples
        --------
            >>> di = prism.estimate.consensus.dataitems('net income')
            >>> di[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0       200203  Net Income (Excl. Extraordinary Items & Good W...
            1       200204  Net Income (Excl. Extraordinary Items & Good W...
            2       200205  Net Income (Excl. Extraordinary Items & Good W...
            3       200206  Net Income (Excl. Extraordinary Items & Good W...
            4       200207  Net Income (Excl. Extraordinary Items & Good W...
            5       200208  Net Income (Excl. Extraordinary Items & Good W...
            6       200209      Net Income (GAAP) - Consensus, # of Estimates
            7       200210                Net Income (GAAP) - Consensus, High
            8       200211                 Net Income (GAAP) - Consensus, Low
            9       200212                Net Income (GAAP) - Consensus, Mean
            10      200213              Net Income (GAAP) - Consensus, Median
            11      200214  Net Income (GAAP) - Consensus, Standard Deviation
            12      200215  Net Income Normalized - Consensus, # of Estimates
            13      200216            Net Income Normalized - Consensus, High
            14      200217             Net Income Normalized - Consensus, Low
            15      200218            Net Income Normalized - Consensus, Mean
            16      200219          Net Income Normalized - Consensus, Median
            17      200220  Net Income Normalized - Consensus, Standard De...
        """
        return cls._dataitems(search=search, package=package)


class growth(_PrismEstimateComponent):
    """
    | Differences in consensus estimate and the actual for a data item.
    | Default frequency is aperiodic.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)
        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

        periodout : int
            | Determines how far out estimate to fetch.
            | For example, inputting 0 will fetch estimate data for the current period, 1 will fetch estimate for the next period.

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the pricing data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.estimate.growth.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       200276  Capital Expenditure - Growth, Quarter on Quart...
        1       200277     Cash Flow / Share - Growth, Annual, 1 Year (%)
        2       200278     Cash Flow / Share - Growth, Annual, 2 Year (%)
        3       200279  Cash Flow / Share - Growth, Quarter on Quarter...
        4       200280     Cash Flow / Share - Growth, Year over Year (%)
        5       200281                   DPS - Growth, Annual, 1 Year (%)
        6       200282                   DPS - Growth, Annual, 2 Year (%)
        7       200283               DPS - Growth, Quarter on Quarter (%)
        8       200284                   DPS - Growth, Year over Year (%)
        9       200285                EBITDA - Growth, Annual, 1 Year (%)
        10      200286                EBITDA - Growth, Annual, 2 Year (%)
        11      200287            EBITDA - Growth, Quarter on Quarter (%)
        12      200288                EBITDA - Growth, Year over Year (%)
        13      200289               Revenue - Growth, Annual, 1 Year (%)
        14      200290               Revenue - Growth, Annual, 2 Year (%)
        15      200291           Revenue - Growth, Quarter on Quarter (%)
        16      200292               Revenue - Growth, Year over Year (%)

        >>> rev_growth = prism.estimate.growth(dataitemid=200281, periodtype='Q')
        >>> rev_growth_df = rev_growth.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> rev_growth_df
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType = None,
        periodout: int = 0,
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the growth data component.


        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.


        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> di = prism.estimate.growth.dataitems()
            >>> di[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0       200276  Capital Expenditure - Growth, Quarter on Quart...
            1       200277     Cash Flow / Share - Growth, Annual, 1 Year (%)
            2       200278     Cash Flow / Share - Growth, Annual, 2 Year (%)
            3       200279  Cash Flow / Share - Growth, Quarter on Quarter...
            4       200280     Cash Flow / Share - Growth, Year over Year (%)
            5       200281                   DPS - Growth, Annual, 1 Year (%)
            6       200282                   DPS - Growth, Annual, 2 Year (%)
            7       200283               DPS - Growth, Quarter on Quarter (%)
            8       200284                   DPS - Growth, Year over Year (%)
            9       200285                EBITDA - Growth, Annual, 1 Year (%)
            10      200286                EBITDA - Growth, Annual, 2 Year (%)
            11      200287            EBITDA - Growth, Quarter on Quarter (%)
            12      200288                EBITDA - Growth, Year over Year (%)
            13      200289               Revenue - Growth, Annual, 1 Year (%)
            14      200290               Revenue - Growth, Annual, 2 Year (%)
            15      200291           Revenue - Growth, Quarter on Quarter (%)
            16      200292               Revenue - Growth, Year over Year (%)
        """
        return cls._dataitems(search=search, package=package)


class recommendation(_PrismEstimateComponent):
    """
    | Recommnedation Data for a data item.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Score, Buy, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> df = prism.estimate.recommendation.dataitems('Score')
        >>> df[['dataitemid', 'dataitemname']]
           dataitemid                     dataitemname
        0      200631           Recommendation - Score
        1      200637  Industry Recommendation - Score
        2      601998           Recommendation - Score
        >>> rec = prism.estimate.recommendation(dataitemid=200631, periodtype='LTM')
        >>> rec.get_data("LSE", "2022-01-01", shownid=['companyname'])
               listingid                 date  Recommendation - Score                     Company Name
        0       22033716  2022-01-01 00:30:00                 2.42105  The Berkeley Group Holdings plc
        1       20131190  2022-01-01 03:29:13                 1.42105         Barratt Developments plc
        2       20175571  2022-01-01 03:29:13                 2.09091                    Elementis plc
        3       25117249  2022-01-01 03:29:13                 2.06250      Lancashire Holdings Limited
        4       29847692  2022-01-01 03:29:13                 2.50000                       Hiscox Ltd
        ...          ...                  ...                     ...                              ...
        63519   20157229  2023-07-31 13:59:44                 2.00000                     RS Group plc
        63520  224316065  2023-07-31 14:31:00                 1.77778                          WPP plc
        63521   20176224  2023-07-31 14:40:11                 2.14286                     Spectris plc
        63522   20157229  2023-07-31 15:11:00                 2.00000                     RS Group plc
        63523   20182531  2023-07-31 17:04:13                 1.76923                      Pearson plc
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType = None,
        package: str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the recommendation data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> di = prism.estimate.recommendation.dataitems()
            >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                         dataitemname
            0      200625    Recommendation - # of Analysts Buy Recommendation
            1      200626    Recommendation - # of Analysts Hold Recommenda...
            2      200627    Recommendation - # of Analysts No Opinion Reco...
            3      200628    Recommendation - # of Analysts Outperform Reco...
            4      200629    Recommendation - # of Analysts Sell Recommenda...
            5      200630    Recommendation - # of Analysts Underperform Re...
            6      200631    Recommendation - Score
            7      200632    Industry Recommendation - # of Analysts Buy Re...
            8      200633    Industry Recommendation - # of Analysts Hold R...
            9      200634    Industry Recommendation - # of Analysts Outper...
            10     200635    Industry Recommendation - # of Analysts Sell R...
            11     200636    Industry Recommendation - # of Analysts Underp...
            12     200637    Industry Recommendation - Score
            13     601991    Recommendation - # of Analysts Buy Recommendation
            14     601993    Recommendation - # of Analysts Hold Recommenda...
            15     601995    Recommendation - # of Analysts Sell Recommenda...
            16     601996    Recommendation - # of Analysts No Opinion Reco...
            17     601997    Recommendation - # of Analysts Total Recommend...
            18     601998    Recommendation - Score
            19     602197    Recommendation - # of Analysts Overweight Reco...
            20     602198    Recommendation - # of Analysts Underweight Rec...
        """
        return cls._dataitems(search=search, package=package)


class guidance(_PrismEstimateComponent):
    """
    | Company guidance data for a data item.
    | Default frequency is aperiodic.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

        periodout : int
            | Determines how far out estimate to fetch.
            | For example, inputting 0 will fetch estimate data for the current period, 1 will fetch estimate for the next period.

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the pricing data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.estimate.guidance.dataitems('eps')
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       200299                          Cash EPS - Guidance, High
        1       200300                           Cash EPS - Guidance, Low
        2       200301                           Cash EPS - Guidance, Mid
        3       200335  EPS (Excl. Extraordinary Items & Good Will) - ...
        4       200336  EPS (Excl. Extraordinary Items & Good Will) - ...
        5       200337  EPS (Excl. Extraordinary Items & Good Will) - ...
        6       200338                        EPS (GAAP) - Guidance, High
        7       200339                         EPS (GAAP) - Guidance, Low
        8       200340                         EPS (GAAP) - Guidance, Mid
        9       200341                    EPS Normalized - Guidance, High
        10      200342                     EPS Normalized - Guidance, Low
        11      200343                     EPS Normalized - Guidance, Mid

        >>> eps = prism.estimate.guidance(dataitemid=200343, periodtype='Q')
        >>> eps_df = eps.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> eps_df
             listingid                 date  EPS Normalized - Guidance, Mid  Ticker
        0      2586546  2013-11-05 21:44:00                            0.45     ANF
        1      2587881  2015-04-08 10:44:00                            0.78      AA
        2      2588077  2010-10-15 11:48:00                            0.05     ATI
        3      2588150  2014-02-06 12:30:00                            2.70     ADS
        4      2588150  2014-04-17 11:30:00                            2.70     ADS
        ..         ...                  ...                             ...     ...
        218   46639516  2015-11-03 03:31:00                            0.82    ATVI
        219   52984459  2011-10-27 13:30:00                            0.51     MJN
        220   52984459  2015-07-14 21:36:00                            0.76     MJN
        221  141637207  2015-07-13 20:30:00                            0.43     XYL
        222  262300822  2015-07-13 20:18:00                            0.40    NAVI
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType = None,
        periodout: int = 0,
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the guidance data component.


        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.


        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> di = prism.estimate.guidance.dataitems('net income')
            >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
            0      200368  Net Income (Excl. Extraordinary Items & Good W...
            1      200369  Net Income (Excl. Extraordinary Items & Good W...
            2      200370  Net Income (Excl. Extraordinary Items & Good W...
            3      200371                 Net Income (GAAP) - Guidance, High
            4      200372                  Net Income (GAAP) - Guidance, Low
            5      200373                  Net Income (GAAP) - Guidance, Mid
            6      200374             Net Income Normalized - Guidance, High
            7      200375              Net Income Normalized - Guidance, Low
            8      200376              Net Income Normalized - Guidance, Mid
        """
        return cls._dataitems(search=search, package=package)


class revision(_PrismEstimateComponent):
    """
    | Revision in consensus estimate a data item.
    | Default frequency is aperiodic.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

        periodout : int
            | Determines how far out estimate to fetch.
            | For example, inputting 0 will fetch estimate data for the current period, 1 will fetch estimate for the next period.

        aggregation : str, {'1 day', '1 week', '1 month', '2 month', '3 month', '3 month latest'}, default '1 day'
            | Aggregation time periods covered in the revisions calculations.

            .. admonition:: Warning
                :class: warning

                | If the input is **'1 week'** the resulting revision Data Component will contain data values that are sum of revision within 1 week of the data dates.
                |
                | If the input is  **'3 month latest'**, it will only account for latest revision of the same analyst. Therefore, if a same analyst revises his/her estimate more than one time within the 3 month period, only one will be counted towards calculating the revision number

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.estimate.revision.dataitems('eps')
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       200408                 Cash EPS - Revision, # of Analysts
        1       200409                          Cash EPS - Revision, Down
        2       200410                     Cash EPS - Revision, No Change
        3       200411      Cash EPS - Revision, Unfiltered # of Analysts
        4       200412               Cash EPS - Revision, Unfiltered Down
        5       200413          Cash EPS - Revision, Unfiltered No Change
        6       200414                 Cash EPS - Revision, Unfiltered Up
        7       200415                            Cash EPS - Revision, Up
        8       200472  EPS (Excl. Extraordinary Items & Good Will) - ...
        9       200473  EPS (Excl. Extraordinary Items & Good Will) - ...
        10      200474  EPS (Excl. Extraordinary Items & Good Will) - ...
        11      200475  EPS (Excl. Extraordinary Items & Good Will) - ...
        12      200476  EPS (Excl. Extraordinary Items & Good Will) - ...
        13      200477  EPS (Excl. Extraordinary Items & Good Will) - ...
        14      200478  EPS (Excl. Extraordinary Items & Good Will) - ...
        15      200479  EPS (Excl. Extraordinary Items & Good Will) - ...
        16      200480               EPS (GAAP) - Revision, # of Analysts
        17      200481                        EPS (GAAP) - Revision, Down
        18      200482                   EPS (GAAP) - Revision, No Change
        19      200483    EPS (GAAP) - Revision, Unfiltered # of Analysts
        20      200484             EPS (GAAP) - Revision, Unfiltered Down
        21      200485        EPS (GAAP) - Revision, Unfiltered No Change
        22      200486               EPS (GAAP) - Revision, Unfiltered Up
        23      200487                          EPS (GAAP) - Revision, Up
        24      200488           EPS Normalized - Revision, # of Analysts
        25      200489                    EPS Normalized - Revision, Down
        26      200490               EPS Normalized - Revision, No Change
        27      200491  EPS Normalized - Revision, Unfiltered # of Ana...
        28      200492         EPS Normalized - Revision, Unfiltered Down
        29      200493    EPS Normalized - Revision, Unfiltered No Change
        30      200494           EPS Normalized - Revision, Unfiltered Up
        31      200495                      EPS Normalized - Revision, Up

        >>> eps = prism.estimate.revision(dataitemid=200495, periodtype='Q')
        >>> eps_df = eps.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> eps_df
                listingid        date   EPS Normalized - Revision, Up  Ticker
        0         2586086  2010-04-20                               1     AFL
        1         2586086  2010-04-21                               1     AFL
        2         2586086  2010-04-22                               1     AFL
        3         2586086  2010-04-29                               2     AFL
        4         2586086  2010-05-01                               1     AFL
        ...           ...         ...                             ...     ...
        126320  306093931  2015-12-05                               1    PYPL
        126321  313064514  2015-11-24                               0     HPE
        126322  313064514  2015-11-26                               3     HPE
        126323  313064514  2015-11-27                               0     HPE
        126324  313064514  2015-12-11                               0     HPE
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType = None,
        periodout: int = 0,
        aggregation: _AggregationType = '1 day',
        package: str = None,
    ):
        if periodtype in ["NTM"]:
            raise PrismValueError(
                f"Revision cannot take {periodtype} as periodtype.",
                valid_list=_PeriodType,
                invalids=["NTM"],
            )
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the revision data component.


        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.
            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> di = prism.estimate.revision.dataitems('net income')
            >>> di[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0       200528  Net Income (Excl. Extraordinary Items & Good W...
            1       200529  Net Income (Excl. Extraordinary Items & Good W...
            2       200530  Net Income (Excl. Extraordinary Items & Good W...
            3       200531  Net Income (Excl. Extraordinary Items & Good W...
            4       200532  Net Income (Excl. Extraordinary Items & Good W...
            5       200533  Net Income (Excl. Extraordinary Items & Good W...
            6       200534  Net Income (Excl. Extraordinary Items & Good W...
            7       200535  Net Income (Excl. Extraordinary Items & Good W...
            8       200536        Net Income (GAAP) - Revision, # of Analysts
            9       200537                 Net Income (GAAP) - Revision, Down
            10      200538            Net Income (GAAP) - Revision, No Change
            11      200539  Net Income (GAAP) - Revision, Unfiltered # of ...
            12      200540      Net Income (GAAP) - Revision, Unfiltered Down
            13      200541  Net Income (GAAP) - Revision, Unfiltered No Ch...
            14      200542        Net Income (GAAP) - Revision, Unfiltered Up
            15      200543                   Net Income (GAAP) - Revision, Up
            16      200544    Net Income Normalized - Revision, # of Analysts
            17      200545             Net Income Normalized - Revision, Down
            18      200546        Net Income Normalized - Revision, No Change
            19      200547  Net Income Normalized - Revision, Unfiltered #...
            20      200548  Net Income Normalized - Revision, Unfiltered Down
            21      200549  Net Income Normalized - Revision, Unfiltered N...
            22      200550    Net Income Normalized - Revision, Unfiltered Up
            23      200551               Net Income Normalized - Revision, Up
        """
        return cls._dataitems(search=search, package=package)


class surprise(_PrismEstimateComponent):
    """
    | Differences in consensus estimate and the actual for a data item.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q',  'NTM', 'YTD', 'Non-Periodic', 'Q-SA'}
            | Estimate Period in which the financial statement results are estimated.
            | An Estimate Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Next twelve months (NTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)
            - Non-Periodic
            - Quarterly and Semi-Annual period (Q-SA) in quarterly standard

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the pricing data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.estimate.surprise.dataitems('revenue')
        >>> di[['dataitemid', 'dataitemname']]
           dataitemid                   dataitemname
        0      200618  Revenue - Surpise, Difference
        1      200619     Revenue - Surpise, Percent

        >>> rev = prism.estimate.surprise(dataitemid=200618, periodtype='Q')
        >>> rev_df = rev.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> rev_df
               listingid      period        date  EPS Normalized - Surpise, Difference  Ticker
        0        2586086  2009-12-31  2010-02-02                                  0.01     AFL
        1        2586086  2010-03-31  2010-04-27                                  0.05     AFL
        2        2586086  2010-06-30  2010-07-27                                  0.01     AFL
        3        2586086  2010-09-30  2010-10-26                                  0.04     AFL
        4        2586086  2010-12-31  2011-02-01                                 -0.01     AFL
          ...          ...         ...         ...                                   ...     ...
        11516  312940617  2014-12-31  2015-01-29                                 -0.25    GOOG
        11517  312940617  2015-03-31  2015-04-23                                 -0.04  GOOC.V
        11518  312940617  2015-03-31  2015-04-23                                 -0.04    GOOG
        11519  312940617  2015-06-30  2015-07-16                                  0.30  GOOC.V
        11520  312940617  2015-06-30  2015-07-16                                  0.30    GOOG
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        currency: str = "report",
        package : str = None,
    ):
        if periodtype in ["NTM", None]:
            raise PrismValueError(
                f"Surprise cannot take {periodtype} as periodtype.",
                valid_list=_PeriodType,
                invalids=["NTM", "None"],
            )
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the surprise data component.


        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                Data items that belong to cash flow statement data component.

            Columns:
                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> di = prism.estimate.surprise.dataitems('net income')
            >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
            0      200612  Net Income (Excl. Extraordinary Items & Good W...
            1      200613  Net Income (Excl. Extraordinary Items & Good W...
            2      200614            Net Income (GAAP) - Surpise, Difference
            3      200615               Net Income (GAAP) - Surpise, Percent
            4      200616        Net Income Normalized - Surpise, Difference
            5      200617           Net Income Normalized - Surpise, Percent
        """
        return cls._dataitems(search=search, package=package)


@_validate_args
def dataitems(search: str = None, package: str = None):
    """
    Usable data items for the estimate data category.

    Parameters
    ----------
        search : str, default None
            | Search word for dataitems name, the search is case-insensitive.

        package : str, default None
            | Search word for package name, the search is case-insensitive.

    Returns
    -------
        pandas.DataFrame
            Data items that belong to cash flow statement data component.

        Columns:
            - *datamodule*
            - *datacomponent*
            - *dataitemid*
            - *datadescription*


    Examples
    --------
        >>> di = prism.estimate.dataitems('net income')
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       200027  Net Income (Excl. Extraordinary Items & Good W...
        1       200028                         Net Income (GAAP) - Actual
        2       200029                     Net Income Normalized - Actual
        3       200203  Net Income (Excl. Extraordinary Items & Good W...
        4       200204  Net Income (Excl. Extraordinary Items & Good W...
        5       200205  Net Income (Excl. Extraordinary Items & Good W...
        6       200206  Net Income (Excl. Extraordinary Items & Good W...
        7       200207  Net Income (Excl. Extraordinary Items & Good W...
        8       200208  Net Income (Excl. Extraordinary Items & Good W...
        9       200209      Net Income (GAAP) - Consensus, # of Estimates
        10      200210                Net Income (GAAP) - Consensus, High
        11      200211                 Net Income (GAAP) - Consensus, Low
        12      200212                Net Income (GAAP) - Consensus, Mean
        13      200213              Net Income (GAAP) - Consensus, Median
    """
    return _list_dataitem(
        datacategoryid=_PrismEstimateComponent.categoryid,
        datacomponentid=None,
        search=search,
        package=package,
    )
