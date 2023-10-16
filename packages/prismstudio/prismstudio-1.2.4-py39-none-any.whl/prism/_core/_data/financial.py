from ..._common.const import FinancialPeriodType as _PeriodType, FinancialPreliminaryType as _FinancialPreliminaryType
from .._req_builder import _list_dataitem
from ..._prismcomponent.prismcomponent import _PrismFinancialComponent, _PrismDataComponent
from ..._utils import _get_params, _validate_args
from ..._utils.exceptions import PrismValueError


__all__ = [
    "balance_sheet",
    "cash_flow",
    "dps",
    # "date",
    "eps",
    "income_statement",
    "segment",
    "ratio",
    "commitment",
    "pension",
    "option",
    "dataitems",
]


_data_category = __name__.split(".")[-1]


class _PrismFinancialDataComponent(_PrismDataComponent, _PrismFinancialComponent):
    _component_category_repr = _data_category

    @classmethod
    def _dataitems(cls, search : str = None, package : str = None):
        return _list_dataitem(
            datacategoryid=cls.categoryid,
            datacomponentid=cls.componentid,
            search=search,
            package=package,
        )


class balance_sheet(_PrismFinancialDataComponent):
    """
    | Data that pertains to a balance sheet portion in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.financial.balance_sheet.dataitems('asset')
            dataitemid                                       dataitemname
        0       100003                           Trading Asset Securities
        1       100012              Finance Division Other Current Assets
        2       100013                        Other Current Assets, Total
        3       100015                       Deferred Tax Assets, Current
        4       100017                               Other Current Assets
        ..         ...                                                ...
        10      100033                                      Assets, Total
        ..         ...                                                ...
        59      100349  Right-of-Use Assets - Operating Lease - Accumu...
        60      100350      Right-of-Use Assets - Operating Lease - Gross
        61      100351        Right-of-Use Assets - Operating Lease - Net
        62      100365                           Trading Asset Securities
        63      100366                           Trading Portfolio Assets

        >>> ta = prism.financial.balance_sheet(dataitemid=100033, periodtype='Q')
        >>> ta_df = ta.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
              listingid        date  currency      period  Assets, Total   Ticker
        0      20108718  2013-05-22       KRW  2013-03-31   9.001210e+11  A004430
        1      20108718  2013-08-21       KRW  2013-06-30   9.132100e+11  A004430
        2      20108718  2013-11-25       KRW  2013-09-30   8.710300e+11  A004430
        3      20108718  2014-03-25       KRW  2013-12-31   8.660220e+11  A004430
        4      20108718  2014-05-15       KRW  2014-03-31   8.890930e+11  A004430
        ...         ...         ...       ...         ...            ...      ...
        4169  278631846  2015-03-31       KRW  2014-12-31   9.511431e+12  A028260
        4170  278631846  2015-05-15       KRW  2015-03-31   8.389397e+12  A028260
        4171  278631846  2015-08-17       KRW  2015-06-30   8.772212e+12  A028260
        4172  278631846  2015-10-15       KRW  2015-09-30   3.926600e+13  A028260
        4173  278631846  2015-11-16       KRW  2015-09-30   3.926658e+13  A028260
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        if periodtype in ["YTD", "LTM"]:
            raise PrismValueError(
                f"Balance Sheet cannot take {periodtype} as periodtype.",
                valid_list=_PeriodType,
                invalids=["YTD", "LTM", "NTM"],
            )
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search : str = None, package : str = None):
        """
        Usable data items for the balance sheet data component.

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
            >>> prism.financial.balance_sheet.dataitems('asset')
                dataitemid  ...                                dataitemdescription
            0       100003  ...  This item represents both debt and equity secu...
            1       100012  ...  This item represents all current assets of a f...
            2       100013  ...                                               None
            3       100015  ...  This item represents the deferred tax conseque...
            4       100017  ...  This item represents current assets other than...
            ..         ...  ...                                                ...
            59      100349  ...                                               None
            60      100350  ...                                               None
            61      100351  ...                                               None
            62      100365  ...                                    Mapped from TAS
            63      100366  ...                                    Mapped from TAP
        """
        return cls._dataitems(search=search, package=package)


class cash_flow(_PrismFinancialDataComponent):
    """
    | Data that pertains to a cash flow statement portion in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.financial.cash_flow.dataitems('free cash')
        >>> di[['dataitemid', 'dataitemname']]
           dataitemid              dataitemname
        0      100506    Free Cash Flow / Share
        1      100513    Levered Free Cash Flow
        2      100544  Unlevered Free Cash Flow

        >>> fps = prism.financial.cash_flow(dataitemid=100506, periodtype='LTM')
        >>> fps_df = fps.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> fps_df
              listingid        date currency      period  Free Cash Flow / Share   Ticker
        0      20108718  2011-03-31      KRW  2010-12-31             -450.948236  A004430
        1      20108718  2012-03-30      KRW  2011-12-31             -585.166666  A004430
        2      20108718  2013-01-15      KRW  2012-12-31             2882.006531  A004430
        3      20108718  2013-03-05      KRW  2012-12-31             2881.166666  A004430
        4      20108718  2013-05-22      KRW  2013-03-31             2087.633126  A004430
        ...         ...         ...      ...         ...                     ...      ...
        4044  277591793  2015-11-16      KRW  2015-09-30           -34806.994056  A000030
        4045  278631846  2015-03-31      KRW  2014-12-31             -553.762978  A028260
        4046  278631846  2015-05-15      KRW  2015-03-31             -818.569872  A028260
        4047  278631846  2015-08-17      KRW  2015-06-30             -221.831704  A028260
        4048  278631846  2015-11-16      KRW  2015-09-30             -705.329630  A028260
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the cash flow statement data component.

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
            >>> prism.financial.cash_flow.dataitems('free cash')
            dataitemid  ...       dataitemdescription
            0      100506  ...                      None
            1      100513  ...    Levered Free Cash Flow
            2      100544  ...  Unlevered Free Cash Flow
        """
        return cls._dataitems(search=search, package=package)


class dps(_PrismFinancialDataComponent):
    """
    | Dividend per share related data.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.financial.dps.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       100547                       Distributable Cash Per Share
        1       100548             Distributable Cash Per Share (Diluted)
        2       100549                                 Dividend Per Share
        3       100550                         Dividend Per Share Class A
        4       100551                         Dividend Per Share Class B
        5       100552                         Special Dividend Per Share
        6       100553         Special Dividend Per Share - Non-Recurring
        7       100554             Special Dividend Per Share - Recurring
        8       100555                 Special Dividend Per Share Class A
        9       100556  Special Dividend Per Share Class A - Non-Recur...
        10      100557     Special Dividend Per Share Class A - Recurring
        11      100558                 Special Dividend Per Share Class B
        12      100559  Special Dividend Per Share Class B - Non-Recur...
        13      100560     Special Dividend Per Share Class B - Recurring

        >>> dps = prism.financial.dps(dataitemid=100549, periodtype='LTM')
        >>> dps_df = dps.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> dps_df
              listingid        date  currency      period  Dividend Per Share   Ticker
        0      20108718  2011-03-31       KRW  2010-12-31                60.0  A004430
        1      20108718  2012-03-30       KRW  2011-12-31                60.0  A004430
        2      20108718  2013-03-05       KRW  2012-12-31                80.0  A004430
        3      20108718  2013-05-22       KRW  2013-03-31                80.0  A004430
        4      20108718  2013-08-21       KRW  2013-06-30                80.0  A004430
        ...         ...         ...       ...         ...                 ...      ...
        3567  277591793  2015-05-15       KRW  2015-03-31               500.0  A000030
        3568  277591793  2015-06-03       KRW  2015-03-31               500.0  A000030
        3569  277591793  2015-08-17       KRW  2015-06-30               750.0  A000030
        3570  277591793  2015-10-29       KRW  2015-09-30               750.0  A000030
        3571  277591793  2015-11-16       KRW  2015-09-30               750.0  A000030
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the dividend per share data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to cash flow statement data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> dpsdi = prism.financial.dps.dataitems()
            >>> dpsdi[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0       100547                       Distributable Cash Per Share
            1       100548             Distributable Cash Per Share (Diluted)
            2       100549                                 Dividend Per Share
            3       100550                         Dividend Per Share Class A
            4       100551                         Dividend Per Share Class B
            5       100552                         Special Dividend Per Share
            6       100553         Special Dividend Per Share - Non-Recurring
            7       100554             Special Dividend Per Share - Recurring
            8       100555                 Special Dividend Per Share Class A
            9       100556  Special Dividend Per Share Class A - Non-Recur...
            10      100557     Special Dividend Per Share Class A - Recurring
            11      100558                 Special Dividend Per Share Class B
            12      100559  Special Dividend Per Share Class B - Non-Recur...
            13      100560     Special Dividend Per Share Class B - Recurring
        """
        return cls._dataitems(search=search, package=package)


# class date(_PrismFinancialDataComponent):
#     """
#     | Relavent dates in the financial statement.
#     | Default frequency is aperiodic daily.

#     Parameters
#     ----------
#         periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
#             | Financial Period in which the financial statement results are reported.
#             | A Financial Period can be of one of the following Period Types:

#             - Annual period (A)
#             - Quarterly period (Q)
#             - Last twelve months (LTM)
#             - Year-to-date (YTD)
#             - Semi-Annual (SA)

#     Returns
#     -------
#         prism._PrismComponent
#             =======================     =====================================================================================================================================================================================================================================================================================
#             Date Type                   Description
#             =======================     =====================================================================================================================================================================================================================================================================================
#             Press Release               Preliminary earnings release. This information is usually released by the company prior to the official filing or release of data.
#             Original                    Original company filing for period. These numbers were the originally filed numbers (not a press release) for this period. In the U.S., this would be represented by a 10K or 10Q SEC filing.
#             Restated                    Results are fundamentally different from the original, i.e., Net Income, Retained Earnings, Total Assets or Cash from Operations are different. Restatements usually happen after an acquisition, divestiture, merger or accounting change.
#             No Change from Original     Appearing again in a later filing, but unchanged from original, or not comparable due to different reporting currencies. These numbers were from a subsequent filing and were recollected but they do not represent changes in the financials that would be considered a restatement.
#             Reclassified                Results somewhat different from original, but bottom line results are the same.
#             =======================     =====================================================================================================================================================================================================================================================================================

#     Examples
#     --------
#         >>> fdate = prism.financial.date('Q')
#         >>> fdate_df = fdate.get_data(universe=1, startdate='2018-01-01')
#         >>> fdate_df
#                  listingid        date      period                 datetype
#         0         20224413  2016-10-27  2015-09-30             Reclassified
#         1         20224413  2016-10-27  2016-09-30                 Original
#         2         20224413  2017-02-08  2015-12-31  No Change from Original
#         3         20224413  2017-02-08  2016-12-31            Press Release
#         4         20224413  2017-03-10  2015-12-31             Reclassified
#         ...            ...         ...         ...                      ...
#         433059  1778113170  2022-09-13  2022-06-30                 Original
#         433060  1786609462  2022-06-07  2021-03-31                 Original
#         433061  1786609462  2022-06-07  2022-03-31                 Original
#         433062  1786609462  2022-08-23  2021-06-30                 Original
#         433063  1786609462  2022-08-23  2022-06-30                 Original
#     """
#     @_validate_args
#     def __init__(
#         self,
#         periodtype: _PeriodType,
#         package : str = None,
#     ):
#         super().__init__(**_get_params(vars()))


class eps(_PrismFinancialDataComponent):
    """
    | Earnings per share related data.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None
    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.financial.eps.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
        0       100561                           Basic Earnings Per Share
        1       100562       Basic Earnings Per Share - Accounting Change
        2       100563   Basic Earnings Per Share - Continuing Operations
        3       100564  Basic Earnings Per Share - Discontinued Operat...
        4       100565     Basic Earnings Per Share - Extraordinary Items
        5       100566  Basic Earnings Per Share - Extraordinary Items...
        6       100567                         Diluted Earnings Per Share
        7       100568     Diluted Earnings Per Share - Accounting Change
        8       100569  Diluted Earnings Per Share - Continuing Operat...
        9       100570  Diluted Earnings Per Share - Discontinued Oper...
        10      100571   Diluted Earnings Per Share - Extraordinary Items
        11      100572  Diluted Earnings Per Share - Extraordinary Ite...
        12      100573                Normalized Basic Earnings Per Share
        13      100574              Normalized Diluted Earnings Per Share
        14      100575                 Reported Basic Earnings Per Share
        15      100576  Reported Basic Earnings Per Share Excl. Extrao...
        16      100577                Reported Diluted Earnings Per Share
        17      100578  Reported Diluted Earnings Per Share Excl. Extr...
        18      100579                                 Revenues Per Share

        >>> eps = prism.financial.eps(dataitemid=100567, periodtype='LTM')
        >>> eps_df = eps.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> eps_df
              listingid        date  currency      period  Diluted Earnings Per Share   Ticker
        0      20108718  2011-03-31       KRW  2010-12-31                  923.751001  A004430
        1      20108718  2012-03-30       KRW  2011-12-31                  418.041666  A004430
        2      20108718  2013-01-15       KRW  2012-12-31                  858.000035  A004430
        3      20108718  2013-03-05       KRW  2012-12-31                  857.750000  A004430
        4      20108718  2013-05-22       KRW  2013-03-31                 1128.355978  A004430
        ...         ...         ...       ...         ...                         ...      ...
        4541  277591793  2015-11-16       KRW  2015-09-30                  764.230312  A000030
        4542  278631846  2015-03-31       KRW  2014-12-31                 4284.419320  A028260
        4543  278631846  2015-05-15       KRW  2015-03-31                  770.272924  A028260
        4544  278631846  2015-08-17       KRW  2015-06-30                  260.679285  A028260
        4545  278631846  2015-11-16       KRW  2015-09-30                23916.737894  A028260
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the earnings per share data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to cash flow statement data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> epsdi = prism.financial.eps.dataitems()
            >>> epsdi[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0       100561                           Basic Earnings Per Share
            1       100562       Basic Earnings Per Share - Accounting Change
            2       100563   Basic Earnings Per Share - Continuing Operations
            3       100564  Basic Earnings Per Share - Discontinued Operat...
            4       100565     Basic Earnings Per Share - Extraordinary Items
            5       100566  Basic Earnings Per Share - Extraordinary Items...
            6       100567                         Diluted Earnings Per Share
            7       100568     Diluted Earnings Per Share - Accounting Change
            8       100569  Diluted Earnings Per Share - Continuing Operat...
            9       100570  Diluted Earnings Per Share - Discontinued Oper...
            10      100571   Diluted Earnings Per Share - Extraordinary Items
            11      100572  Diluted Earnings Per Share - Extraordinary Ite...
            12      100573                Normalized Basic Earnings Per Share
            13      100574              Normalized Diluted Earnings Per Share
            14      100575                 Reported Basic Earnings Per Share
            15      100576  Reported Basic Earnings Per Share Excl. Extrao...
            16      100577                Reported Diluted Earnings Per Share
            17      100578  Reported Diluted Earnings Per Share Excl. Extr...
            18      100579                                 Revenues Per Share
        """
        return cls._dataitems(search=search, package=package)


class income_statement(_PrismFinancialDataComponent):
    """
    | Data that pertains to a income statement portion in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.financial.income_statement.dataitems('net income')
            dataitemid                             dataitemname
        0       100637                    Net Income to Company
        1       100639                               Net Income
        2       100644          Other Adjustments to Net Income
        3       100645  Net Income Allocable to General Partner
        4       100646   Net Income to Common Incl. Extra Items
        5       100647   Net Income to Common Excl. Extra Items
        6       100703                       Diluted Net Income
        7       100829                               Net Income
        8       100830               Net Income as per SFAS 123
        9       100831  Net Income from Discontinued Operations
        10      100842                    Normalized Net Income

        >>> ni = prism.financial.income_statement(dataitemid=100639, periodtype='LTM')
        >>> ni_df = ni.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ni_df
              listingid        date currency      period    Net Income   Ticker
        0      20108718  2011-03-31      KRW  2010-12-31  2.217002e+10  A004430
        1      20108718  2012-03-30      KRW  2011-12-31  1.003300e+10  A004430
        2      20108718  2013-01-15      KRW  2012-12-31  2.058600e+10  A004430
        3      20108718  2013-03-05      KRW  2012-12-31  2.058600e+10  A004430
        4      20108718  2013-05-22      KRW  2013-03-31  2.714800e+10  A004430
        ...         ...         ...      ...         ...           ...      ...
        4619  278631846  2015-03-31      KRW  2014-12-31  4.556470e+11  A028260
        4620  278631846  2015-05-15      KRW  2015-03-31  8.384555e+10  A028260
        4621  278631846  2015-08-17      KRW  2015-06-30  2.902545e+10  A028260
        4622  278631846  2015-10-15      KRW  2015-09-30  2.820902e+12  A028260
        4623  278631846  2015-11-16      KRW  2015-09-30  2.822057e+12  A028260
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the income statement data component.

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
            >>> prism.financial.income_statement.dataitems('income')
                dataitemid  ...                                dataitemdescription
            0       100586  ...  This item represents the interest and investme...
            1       100588  ...  This item represents fee from non-fund based a...
            2       100607  ...  This item represents all other operating expen...
            3       100610  ...  This item represents the difference between th...
            4       100612  ...  This item represents the interest and investme...
            ..         ...  ...                                                ...
            71      100902  ...                                               None
            72      100903  ...  This item represents the total sub-lease incom...
            73      100904  ...  This item represents Taxes other than excise a...
            74      100905  ...  This item represents all taxes other than inco...
            75      100906  ...  This item represents refund of any tax amount ...
        """
        return cls._dataitems(search=search, package=package)


class segment(_PrismFinancialDataComponent):
    """
    | Data that pertains to a specific segment or division within a company.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> segment = prism.financial.segment.dataitems()
        >>> segment[['dataitemid', 'dataitemname']]
           dataitemid                                     dataitemname
        0      104729                        Business Segments - CAPEX
        1      104730  Business Segments - Depreciation & Amortization
        2      104731                       Business Segments - EBITDA
        3      104732                          Business Segments - EBT
        4      104733                 Business Segments - Gross Profit
        5      104734           Business Segments - Income Tax Expense
        6      104735             Business Segments - Interest Expense
        7      104736                        Business Segments - NOPAT
        8      104737                   Business Segments - Net Income
        >>> seg = prism.financial.segment(104731, periodtype='Q')
        >>> seg.get_data(universe=1, startdate='2010-01-01', enddate='2015-01-01', shownid=['ticker'])
           listingid        date            segment  latestperiod  currency  Business Segments - EBITDA: 0 Quarters Back   Ticker
        0  144523336  2013-01-31  Convenience Store    2012-12-31       KRW                                 4.920000e+10  A007070
        1  144523336  2013-01-31        Supermarket    2012-12-31       KRW                                 6.900000e+09  A007070
        2  144523336  2013-03-29  Convenience Store    2012-12-31       KRW                                 4.920000e+10  A007070
        3  144523336  2013-03-29        Supermarket    2012-12-31       KRW                                 6.900000e+09  A007070
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the segment data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to segment data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> segdi = prism.financial.segment.dataitems()
            >>> segdi[['dataitemid', 'dataitemname']]
            dataitemid                                     dataitemname
            0      104729                        Business Segments - CAPEX
            1      104730  Business Segments - Depreciation & Amortization
            2      104731                       Business Segments - EBITDA
            3      104732                          Business Segments - EBT
            4      104733                 Business Segments - Gross Profit
            5      104734           Business Segments - Income Tax Expense
            6      104735             Business Segments - Interest Expense
            7      104736                        Business Segments - NOPAT
            8      104737                   Business Segments - Net Income
        """
        return cls._dataitems(search=search, package=package)


class ratio(_PrismFinancialDataComponent):
    """
    | Data that pertains to a ratio data in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> ratdi = prism.financial.ratio.dataitems()
        >>> ratdi[['dataitemid', 'dataitemname']]
             dataitemid                                       dataitemname
        0        104934                       Annualized Dividend Payout %
        1        104935                      Annualized Dividend Per Share
        2        104936                        Annualized Dividend Yield %
        3        104937    3 Yr. Compound Net Capital Expenditure Growth %
        4        104938    5 Yr. Compound Net Capital Expenditure Growth %
        ...         ...                                                ...
        303      112907                        Liabilities / Assets, Total
        304      113691                Net Working Capital / Total Revenue
        305      113692                 Net Working Capital / Total Assets
        306      113695                           Working Capital Turnover
        307      114803  Altman Z Score Using the Average Stock Informa...
        >>> rat = prism.financial.ratio(112907, periodtype='Q')
        >>> rat.get_data(universe=1, startdate='2010-01-01', enddate='2015-01-01', shownid=['ticker'])
               listingid        date  latestperiod  Liabilities / Assets, Total: 0 Quarters Back   Ticker
        0       20216251  2010-01-01    2009-09-30                                       82.1596     None
        1       49782109  2010-01-06    2009-09-30                                       10.7062     None
        2       20168002  2010-01-08    2009-09-30                                       93.1549  A005350
        3       31779033  2010-01-11    2009-09-30                                       37.3517  A050470
        4       31779068  2010-01-12    2009-09-30                                       49.1868  A056080
        ...          ...         ...           ...                                           ...      ...
        22657  224013404  2014-12-31    2014-09-30                                       67.5691  A141070
        22658  237676086  2014-12-31    2014-09-30                                       35.5406  A158380
        22659  248503946  2014-12-31    2014-09-30                                       38.1093  A131970
        22660  248629939  2014-12-31    2014-09-30                                        8.8119  A171120
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the ratio data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to ratio data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> ratdi = prism.financial.segment.dataitems()
            >>> ratdi[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0        104934                       Annualized Dividend Payout %
            1        104935                      Annualized Dividend Per Share
            2        104936                        Annualized Dividend Yield %
            3        104937    3 Yr. Compound Net Capital Expenditure Growth %
            4        104938    5 Yr. Compound Net Capital Expenditure Growth %
            ...         ...                                                ...
            303      112907                        Liabilities / Assets, Total
            304      113691                Net Working Capital / Total Revenue
            305      113692                 Net Working Capital / Total Assets
            306      113695                           Working Capital Turnover
            307      114803  Altman Z Score Using the Average Stock Informa...
        """
        return cls._dataitems(search=search, package=package)


class commitment(_PrismFinancialDataComponent):
    """
    | Data that pertains to a commitment related data (such as operating leases etc.) in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> comdi = prism.financial.commitment.dataitems()
        >>> comdi[['dataitemid', 'dataitemname']]
             dataitemid                               dataitemname
        0        104830     Capital Lease Payment Due, Current Yr.
        1        104831  Capital Lease Payment Due, Current Yr. +1
        2        104832  Capital Lease Payment Due, Current Yr. +2
        3        104833  Capital Lease Payment Due, Current Yr. +3
        4        104834  Capital Lease Payment Due, Current Yr. +4
        ...         ...                                        ...
        117      500282                     Year 1 - (Annual Only)
        118      500283                     Year 2 - (Annual Only)
        119      500284                     Year 3 - (Annual Only)
        120      500285                     Year 4 - (Annual Only)
        121      500286                     Year 5 - (Annual Only)
        >>> com = prism.financial.commitment(104830, periodtype='Q')
        >>> com.get_data(universe=1, startdate='2010-01-01', enddate='2015-01-01', shownid=['ticker'])
               listingid        date  latestperiod  currency  Capital Lease Payment Due, Current Yr.: 0 Quarters Back   Ticker
        0       20216251  2010-01-01    2009-09-30       KRW                                                      NaN     None
        1       49782109  2010-01-06    2009-09-30       KRW                                                      NaN     None
        2       20168002  2010-01-08    2009-09-30       KRW                                                      NaN  A005350
        3       31779033  2010-01-11    2009-09-30       KRW                                                      NaN  A050470
        4       31779068  2010-01-12    2009-09-30       KRW                                                      NaN  A056080
        ...          ...         ...           ...       ...                                                      ...      ...
        22657  224013404  2014-12-31    2014-09-30       KRW                                                      NaN  A141070
        22658  237676086  2014-12-31    2014-09-30       KRW                                                      NaN  A158380
        22659  248503946  2014-12-31    2014-09-30       KRW                                                      NaN  A131970
        22660  248629939  2014-12-31    2014-09-30       KRW                                                      NaN  A171120
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the commitment data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to commitment data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> comdi = prism.financial.commitment.dataitems()
            >>> comdi[['dataitemid', 'dataitemname']]
                dataitemid                               dataitemname
            0        104830     Capital Lease Payment Due, Current Yr.
            1        104831  Capital Lease Payment Due, Current Yr. +1
            2        104832  Capital Lease Payment Due, Current Yr. +2
            3        104833  Capital Lease Payment Due, Current Yr. +3
            4        104834  Capital Lease Payment Due, Current Yr. +4
            ...         ...                                        ...
            117      500282                     Year 1 - (Annual Only)
            118      500283                     Year 2 - (Annual Only)
            119      500284                     Year 3 - (Annual Only)
            120      500285                     Year 4 - (Annual Only)
            121      500286                     Year 5 - (Annual Only)
        """
        return cls._dataitems(search=search, package=package)


class pension(_PrismFinancialDataComponent):
    """
    | Data that pertains to a pension related data in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> pendi = prism.financial.pension.dataitems()
        >>> pendi[['dataitemid', 'dataitemname']]
             dataitemid                                       dataitemname
        0        100299                          Minimum Pension Liability
        1        100370    Un-funded Vested Pension Liabilities - Domestic
        2        100371     Un-funded Vested Pension Liabilities - Foreign
        3        100741  Expected Rate of Return on Pension Assets - Do...
        4        100742  Expected Rate of Return on Pension Assets - Fo...
        ...         ...                                                ...
        592      500346              Net Liability/(Asset) - (Annual Only)
        593      500347               Unfunded Liabilities - (Annual Only)
        594      500348     Expected Return on Plan Assets - (Annual Only)
        595      500349       Actual Return on Plan Assets - (Annual Only)
        596      500350  Expected LT Return Rate on Plan Assets (%) - (...
        >>> pen = prism.financial.pension(104830, periodtype='Q')
        >>> pen.get_data(universe=1, startdate='2010-01-01', enddate='2015-01-01', shownid=['ticker'])
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the pension data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to pension data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> pendi = prism.financial.pension.dataitems()
            >>> pendi[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0        100299                          Minimum Pension Liability
            1        100370    Un-funded Vested Pension Liabilities - Domestic
            2        100371     Un-funded Vested Pension Liabilities - Foreign
            3        100741  Expected Rate of Return on Pension Assets - Do...
            4        100742  Expected Rate of Return on Pension Assets - Fo...
            ...         ...                                                ...
            592      500346              Net Liability/(Asset) - (Annual Only)
            593      500347               Unfunded Liabilities - (Annual Only)
            594      500348     Expected Return on Plan Assets - (Annual Only)
            595      500349       Actual Return on Plan Assets - (Annual Only)
            596      500350  Expected LT Return Rate on Plan Assets (%) - (...
        """
        return cls._dataitems(search=search, package=package)


class option(_PrismFinancialDataComponent):
    """
    | Data that pertains to a options and warrants related data in financial statement.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.
            | A Financial Period can be of one of the following Period Types:

            - Annual period (A)
            - Quarterly period (Q)
            - Last twelve months (LTM)
            - Year-to-date (YTD)
            - Semi-Annual (SA)

        preliminary : str, {'keep', 'ignore', 'null'}, default 'keep'
            - keep : keep preliminary data
            - ignore : ignore preliminary data

            .. admonition:: Note
                :class: note

                | If the 'ignore' option is chosen, preliminary reports are disregarded entirely, as if they never existed.
                |
                | Consequently, if a revision occurs on the same day as the preliminary report, the latest period (period 0) will continue to display the previous period of preliminary reporting, and it will not be updated until the official report is released.

            - null : nulled-out preliminary data

        currency : str, {'report', 'trade', ISO3 currency}, default 'report'
            | Desired currency for the financial data.

            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

            .. admonition:: Warning
                :class: warning

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored.
                | It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> optdi = prism.financial.option.dataitems()
        >>> optdi[['dataitemid', 'dataitemname']]
             dataitemid                                       dataitemname
        0        100668                       Average Price paid per Share
        1        100883                  Shares Purchased - Quarter, Total
        2        104885                       Stock Options Exercise Price
        3        104886                          Stock Options Grant Price
        4        104898  Stock Options Outstanding At The Beginning of ...
        ...         ...                                                ...
        109      107688    Exercisable Warrants W / Average Exercise Price
        110      107689  Exercisable Warrants W / Average Remaining Lif...
        111      107690     Outstanding Warrants Aggregate Intrinsic Value
        112      107691     Exercisable Warrants Aggregate Intrinsic Value
        113      107693                             Stock Option Plan Name
        >>> opt = prism.financial.pension(100668, periodtype='Q')
        >>> opt.get_data(universe=1, startdate='2010-01-01', enddate='2015-01-01', shownid=['ticker'])
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        periodtype: _PeriodType,
        preliminary: _FinancialPreliminaryType = "keep",
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the option data component.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                | Search word for package name, the search is case-insensitive.

        Returns
        -------
            pandas.DataFrame
                | Data items that belong to option data component.

            Columns:

                - *datamodule*
                - *datacomponent*
                - *dataitemid*
                - *datadescription*

        Examples
        --------
            >>> optdi = prism.financial.option.dataitems()
            >>> optdi[['dataitemid', 'dataitemname']]
                dataitemid                                       dataitemname
            0        100668                       Average Price paid per Share
            1        100883                  Shares Purchased - Quarter, Total
            2        104885                       Stock Options Exercise Price
            3        104886                          Stock Options Grant Price
            4        104898  Stock Options Outstanding At The Beginning of ...
            ...         ...                                                ...
            109      107688    Exercisable Warrants W / Average Exercise Price
            110      107689  Exercisable Warrants W / Average Remaining Lif...
            111      107690     Outstanding Warrants Aggregate Intrinsic Value
            112      107691     Exercisable Warrants Aggregate Intrinsic Value
            113      107693                             Stock Option Plan Name
        """
        return cls._dataitems(search=search, package=package)


@_validate_args
def dataitems(search: str = None, package: str = None):
    """
    Usable data items for the financial data category.

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
    >>> prism.financial.dataitems('revenue')
        dataitemid  ...                                dataitemdescription
    0       100044  ...  This item represents revenues, which are recei...
    1       100053  ...  This item represents revenues which are receiv...
    2       100196  ...  This item represents revenues relating to peri...
    3       100228  ...  This item represents the portion of realized r...
    4       100263  ...  This item represents the bonds which are issue...
    5       100408  ...  This item represents change in revenues relati...
    6       100483  ...                                From AP Tag CFURXNC
    7       100579  ...                                  Revenue Per Share
    8       100580  ...  This item represents the total revenues that a...
    9       100581  ...                                               None
    10      100582  ...  This item represents the revenues generated by...
    11      100583  ...  This item represents revenues generated by the...
    """
    return _list_dataitem(
            datacategoryid=_PrismFinancialDataComponent.categoryid,
            datacomponentid=None,
            search=search,
            package=package,
        )
