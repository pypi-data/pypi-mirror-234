from .financial import _PrismFinancialDataComponent
from .._req_builder import _list_dataitem
from ..._common.const import FinancialPeriodType as _PeriodType, FinancialPreliminaryType as _FinancialPreliminaryType
from ..._utils import _validate_args, _get_params


__all__ = [
    'airlines',
    'bank',
    'capital_market',
    'financial_services',
    'healthcare',
    'homebuilders',
    'hotel',
    'insurance',
    'internet',
    'managed_care',
    'mining',
    'oil',
    'biopharma',
    'real_estate',
    'restaurant',
    'retail',
    'semiconductors',
    'telecom',
    'utility',
    'dataitems',
]


_data_category = __name__.split(".")[-1]


class _PrismIndustryFinancialDataComponent(_PrismFinancialDataComponent):
    _component_category_repr = _data_category


class airlines(_PrismIndustryFinancialDataComponent):
    """
    | Return the airline industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.airlines.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid	                             dataitemname
        0        100916              Aircraft Average Age (Years)
        1        100917	                          Aircraft Leased
        2        100918	                  Aircraft Not in Service
        3        100919	                           Aircraft Owned
        4        100920	         Aircraft Retired during the Year
        5        100921	                       Aircraft Subleased
        6        100922	                  Aircraft, Capital Lease
        7        100923	                    Aircraft, Firm Orders
        ...         ...                                       ...
        46       100962                   Fuel Consumed (Gallons)
        47       100963                    Fuel Consumed (Liters)
        48       100964                        Fuel Cost / Gallon
        49       100965                         Fuel Cost / Liter
        50       100966                              Fuel Expense
        51       100967  Fuel Expense as a % of Operating Expense
        52       100968                             Fuel Expenses

        >>> ta = prism.industry.airlines(dataitemid=100922, periodtype='Q')
        >>> ta_df = ta.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
            listingid        date      period  Fuel Consumed (Gallons)	Ticker
        0     2651692  2010-01-21  2009-12-31	          3.450000e+08     LUV
        1     2651692  2010-04-22  2010-03-31             3.290000e+08     LUV
        2     2651692  2010-04-26  2010-03-31             3.290000e+08     LUV
        3     2651692  2010-07-29  2010-06-30             3.720000e+08     LUV
        4     2651692  2010-08-02  2010-06-30             3.720000e+08     LUV
        5     2651692  2010-10-21  2010-09-30             3.750000e+08     LUV
        ...       ...         ...         ...                      ...     ...
        54   34058542  2015-07-15  2015-06-30             1.029000e+09     DAL
        55   34058542  2015-10-14  2015-09-30             1.096000e+09     DAL
        56  252670109  2015-04-24  2015-03-31             1.013000e+09     AAL
        57  252670109  2015-07-24  2015-06-30             1.118000e+09     AAL
        58  252670109  2015-10-23  2015-09-30             1.140000e+09     AAL
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
        Usable data items for the airlines industry specific data component.

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
            >>> di = prism.industry.airlines.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
                dataitemid                              dataitemname
            0       100916              Aircraft Average Age (Years)
            1       100917                           Aircraft Leased
            2       100918                   Aircraft Not in Service
            3       100919                            Aircraft Owned
            ...        ...                                       ...
            50      100966                              Fuel Expense
            51      100967  Fuel Expense as a % of Operating Expense
            52      100968                             Fuel Expenses
        """
        return cls._dataitems(search=search, package=package)


class bank(_PrismIndustryFinancialDataComponent):
    """
    | Return the bank industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.bank.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
               dataitemid	               dataitemname
        0	       100969	       Cash and Equivalents
        1	       100970	      Investment Securities
        2	       100971	   Trading Asset Securities
        3	       100972  Mortgage Backed Securities
        4	       100973	         investments, Total
        ...	          ...	                        ...
        371        101340	         Non, Accrual Loans
        372        101341	      Non-Performing Assets
        373	       101342	       Non-Performing Loans
        374	       101343	         Restructured Loans
        375	       101344	         Specific Allowance

        >>> ta = prism.industry.bank(dataitemid=100971, periodtype='Q')
        >>> ta_df = ta.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
              listingid	       date	 currency	     period  Trading Asset Securities    Ticker
        0       2586086	 2010-05-07	      USD	 2010-03-31	               73000000.0	    AFL
        1       2586086	 2010-08-02	      USD	 2010-06-30	               97000000.0	    AFL
        2       2586086	 2010-11-05	      USD	 2010-09-30	              118000000.0	    AFL
        3       2586086	 2011-02-25	      USD	 2010-12-31	              124000000.0	    AFL
        4       2586086	 2011-04-27	      USD	 2010-03-31	              124000000.0	    AFL
        ...	        ...	        ...	      ...	        ...	                      ...	    ...
        4682  325621650	 2014-06-10	      USD	 2013-06-30	               14000000.0	   AVGO
        4683  325621650	 2014-08-28	      USD	 2013-06-30	               14000000.0	   AVGO
        4684  325621650	 2014-09-12	      USD	 2013-06-30	               14000000.0	   AVGO
        4685  325621650	 2015-02-25	      USD	 2013-12-31	               14000000.0	   AVGO
        4686  325621650  2015-03-11	      USD	 2013-12-31	               14000000.0	   AVGO
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
        Usable data items for the bank industry specific data component.

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
            >>> di = prism.industry.bank_dataitems()
            >>> di[["dataitemid", "dataitemname"]]
                dataitemid                dataitemname
            0        100969        Cash and Equivalents
            1        100970       Investment Securities
            2        100971    Trading Asset Securities
            3        100972  Mortgage Backed Securities
            4        100973          investments, Total
            ...         ...                         ...
            371      101340          Non, Accrual Loans
            372      101341       Non-Performing Assets
            373      101342        Non-Performing Loans
            374      101343          Restructured Loans
            375      101344          Specific Allowance
        """
        return cls._dataitems(search=search, package=package)


class capital_market(_PrismIndustryFinancialDataComponent):
    """
    | Return the capital market specific data from financial statement.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.
            | This identifies the type of the balance sheet value (Revenue, Expense, etc.)

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
        >>> di = prism.industry.capital_market.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
               dataitemid	                           dataitemname
        0          101345	                Assets Under Management
        1	       101346	                           Equity Funds
        2	       101347	                     Fixed Income Funds
        3	       101348	                     Money Market Funds
        4	       101349	                            Other Funds
        ...	          ...	                                    ...
        225	       101570	 Daily Average Revenue Trades, (DARTs')
        226	       101571	                  Net New Client Assets
        227	       101572	              Number of Trades Executed
        228	       101573	                    Organic Growth Rate
        229	       101574	               Value of Customer Assets

        >>> ta = prism.industry.capital_market(dataitemid=101348, periodtype='Q')
        >>> ta_df = ta.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
               listingid        date    currency	  period    Money Market Funds  Ticker
        0	     2592914  2010-01-20	     USD  2009-12-31	      1.791120e+11     BAC
        1	     2592914  2010-04-16	     USD  2010-03-31	      1.585770e+11	   BAC
        2	     2592914  2010-07-16	     USD  2010-06-30	      1.479610e+11	   BAC
        3	     2592914  2015-07-29	     USD  2015-06-30	      8.131400e+10	   BAC
        4	     2592914  2015-10-14	     USD  2015-09-30	      7.810600e+10	   BAC
        ...	         ...	     ...	     ...         ...	               ...	   ...
        573	    39385806  2015-01-29	     USD  2014-12-31	      7.650000e+10	   IVZ
        574	    39385806  2015-02-20	     USD  2014-12-31	      7.650000e+10	   IVZ
        575	    39385806  2015-04-30	     USD  2015-03-31	      7.020000e+10	   IVZ
        576	    39385806  2015-07-30	     USD  2015-06-30	      6.790000e+10	   IVZ
        577	    39385806  2015-10-29         USD  2015-09-30	      6.680000e+10	   IVZ
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
        Usable data items for the capital market industry specific data component.

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
            >>> di = prism.industry.capital_market.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                            dataitemname
            0      101345                 Assets Under Management
            1      101346                            Equity Funds
            2      101347                      Fixed Income Funds
            3      101348                      Money Market Funds
            4      101349                             Other Funds
            ...       ...                                     ...
            225    101570  Daily Average Revenue Trades, (DARTs')
            226    101571                   Net New Client Assets
            227    101572               Number of Trades Executed
            228    101573                     Organic Growth Rate
            229    101574                Value of Customer Assets
        """
        return cls._dataitems(search=search, package=package)


class financial_services(_PrismIndustryFinancialDataComponent):
    """
    | Return the financial services industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.financial_services.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
               dataitemid                               dataitemname
        0	       101575	                    Cash and Equivalents
        1	       101576	                   Long-term Investments
        2	       101577	                Trading Asset Securities
        3	       101578	             Loans and Lease Receivables
        4	       101579	                       Other Receivables
        ...	          ...	                                     ...
        182	       101757	       Other Preferred Stock Adjustments
        183	       101758	         Other Adjustments to Net Income
        184	       101759    Net Income Allocable to General Partner
        185	       101760     Net Income to Common Incl. Extra Items
        186	       101761	  Net Income to Common Excl. Extra Items

        >>> ta = prism.industry.financial_services(dataitemid=101579, periodtype='Q')
        >>> ta_df = ta.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
                listingid	       date  currency	     period	Other Receivables	 Ticker
        0	      2586086    2010-02-26	      USD	 2009-12-31	      764000000.0	    AFL
        1	      2586086    2010-08-02	      USD	 2010-06-30	      659000000.0	    AFL
        2	      2586086    2010-11-05	      USD	 2010-09-30	      640000000.0	    AFL
        3	      2586086    2011-02-01	      USD	 2009-12-31	      640000000.0	    AFL
        4	      2586086    2011-02-25	      USD	 2010-12-31	      661000000.0	    AFL
        ...	          ...	        ...	      ...	        ...	              ...	    ...
        7700    344286611	 2011-04-29	      USD	 2010-03-31	       47000000.0	    ITT
        7701    344286611    2011-05-02	      USD	 2011-03-31	       47000000.0	    ITT
        7702    344286611	 2011-07-29	      USD	 2010-06-30	       47000000.0	    ITT
        7703    344286611	 2011-08-01	      USD	 2011-06-30	       45000000.0	    ITT
        7704    344286611	 2011-10-28	      USD	 2011-09-30	       43000000.0	    ITT
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
        Usable data items for the financial services industry specific data component.

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
            >>> di = prism.industry.financial_services.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                             dataitemname
            0      101575                     Cash and Equivalents
            1      101576                    Long-term Investments
            2      101577                 Trading Asset Securities
            3      101578              Loans and Lease Receivables
            4      101579                        Other Receivables
            ...       ...                                      ...
            182    101757        Other Preferred Stock Adjustments
            183    101758          Other Adjustments to Net Income
            184    101759  Net Income Allocable to General Partner
            185    101760   Net Income to Common Incl. Extra Items
            186    101761   Net Income to Common Excl. Extra Items
        """
        return cls._dataitems(search=search, package=package)


class healthcare(_PrismIndustryFinancialDataComponent):
    """
    | Return the healthcare industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.healthcare.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid	                                dataitemname
        0 	     101762                            ASO Covered Lives
        1	     101763	                        Covered Lives, Total
        2	     101764	                          Risk Covered Lives
        3	     101765	                          Inpatient Services
        4	     101766                     Other Operating Expenses
        .. 	        ...	                                         ...
        84	     101846	     Unconsolidated Hospitals and Facilities
        85	     101847	                        Growth in Admissions
        86	     101848	             Growth in Equivalent Admissions
        87	     101849	 Growth in Revenue per Equivalent Admissions
        88	     101850	                          Growth in Revenues

        >>> ta = prism.industry.healthcare(dataitemid=101766, periodtype='Q')
        >>> ta_df = ta.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
            listingid        date      period  Other Operating Expenses  Ticker
        0     2657437  2010-02-23  2009-12-31                      21.3     THC
        1     2657437  2010-05-04  2010-03-31                      19.9     THC
        2     2657437  2010-08-03  2010-06-30                      21.6     THC
        3     2657437  2010-11-02  2010-09-30                      22.3     THC
        4     2657437  2011-02-25  2010-12-31                      20.3     THC
        5     2657437  2011-05-03  2011-03-31                      20.3     THC
        ..        ...         ...         ...                       ...     ...
        30    2661198  2015-08-07  2015-06-30                      23.5     UHS
        31    2661198  2015-10-27  2015-09-30                      23.8     UHS
        32    2661198  2015-11-06  2015-09-30                      23.8     UHS
        33  128219751  2015-02-03  2014-12-31                      18.5     HCA
        34  128219751  2015-05-05  2015-03-31                      17.7     HCA
        35  128219751  2015-08-05  2015-06-30                      17.7     HCA
        36  128219751  2015-10-27  2015-09-30                      18.2     HCA
        37  128219751  2015-10-29  2015-09-30                      18.2     HCA
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
        Usable data items for the healthcare industry specific data component.

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
            >>> di = prism.industry.healthcare.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                 dataitemname
            0      101762                            ASO Covered Lives
            1      101763                         Covered Lives, Total
            2      101764                           Risk Covered Lives
            3      101765                           Inpatient Services
            4      101766                     Other Operating Expenses
            ...       ...                                          ...
            84     101846      Unconsolidated Hospitals and Facilities
            85     101847                         Growth in Admissions
            86     101848              Growth in Equivalent Admissions
            87     101849  Growth in Revenue per Equivalent Admissions
            88     101850                           Growth in Revenues
        """
        return cls._dataitems(search=search, package=package)


class homebuilders(_PrismIndustryFinancialDataComponent):
    """
    | Return the homebuilders industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.homebuilders.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid	                                      dataitemname
        0	     101851	                                  Homes in Backlog
        1	     101852	                   Homes in  Backlog Average Price
        2	     101853	         Homes in Backlog Average Price, Incl. JVs
        3	     101854       	       Homes in Backlog Average Price, JVs
        4	     101855	                            Homes in Backlog Value
        ...	        ...	                                               ...
        134	     101985	        Warranty Reserves Issued During the Period
        135	     101986	 Warranty Reserves Other Adjustments During the...
        136	     101987	      Warranty Reserves Payments During the Period
        137	     101988	  Warranty Reserves at the Beginning of the Period
        138	     101989	        Warranty Reserves at the End of the Period

        >>> ta = prism.industry.homebuilders(dataitemid=101855, periodtype='Q')
        >>> ta_df = ta.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
             listingid	      date  currency	    period  Homes in Backlog Value	Ticker
        0	   2604698  2010-02-02	     USD	2009-12-31	          8.840000e+08	   DHI
        1	   2604698	2010-04-30	     USD	2010-03-31            1.306900e+09	   DHI
        2	   2604698	2010-08-03	     USD  2010-06-30	          9.544000e+08	   DHI
        3	   2604698	2010-11-12       USD  2010-09-30	          8.508000e+08	   DHI
        4	   2604698	2011-01-27	     USD	2010-12-31	          7.954000e+08	   DHI
        ..         ...	       ...	     ...	       ...                     ...	   ...
        97 	   2641195	2014-10-23	     USD	2014-09-30            2.615288e+09	   PHM
        98	   2641195	2015-01-29	     USD	2014-12-31            1.943861e+09	   PHM
        99	   2641195	2015-04-23	     USD	2015-03-31	          2.564092e+09	   PHM
        100	   2641195	2015-07-23	     USD    2015-06-30	          3.087862e+09	   PHM
        101	   2641195	2015-10-22	     USD	2015-09-30	          3.089054e+09	   PHM
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
        Usable data items for the homebuilders industry specific data component.

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
            >>> di = prism.industry.homebuilders.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
                dataitemid                                       dataitemname
            0        101851                                   Homes in Backlog
            1        101852                     Homes in Backlog Average Price
            2        101853          Homes in Backlog Average Price, Incl. JVs
            3        101854                Homes in Backlog Average Price, JVs
            4        101855                             Homes in Backlog Value
            ..          ...                                                ...
            134      101985         Warranty Reserves Issued During the Period
            135      101986  Warranty Reserves Other Adjustments During the...
            136      101987       Warranty Reserves Payments During the Period
            137      101988   Warranty Reserves at the Beginning of the Period
            138      101989         Warranty Reserves at the End of the Period
        """
        return cls._dataitems(search=search, package=package)


class hotel(_PrismIndustryFinancialDataComponent):
    """
    | Return the hotel and gaming industry specific data from financial statement.
    | Default frequency is quarterly.

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

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored. It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.industry.hotel.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid                     dataitemname
        0        101990  Average Number of Slot Machines
        1        101991         Average Number of Tables
        2        101992        Casinos, Incl. JVs, Total
        3        101993                     Casinos, JVs
        4        101994   Gaming Space, Incl. JVs, Total
        ..          ...                              ...
        201      102191                     Rooms Closed
        202      102192                     Rooms Opened
        203      102193                       Rooms Sold
        204      102194               Rooms at Beginning
        205      102195                     Rooms, Total

        >>> ta = prism.industry.hotel(dataitemid=102195, periodtype='Q')
        >>> ta_df = ta.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
             listingid        date      period  Rooms, Total  Ticker
        0      2619070  2010-02-17  2009-12-31       64668.0     HST
        1      2619070  2010-04-28  2010-03-31       64292.0     HST
        2      2619070  2010-07-21  2010-06-30       63984.0     HST
        3      2619070  2010-10-13  2010-09-30       65500.0     HST
        4      2619070  2011-02-15  2010-12-31       65500.0     HST
        ..         ...         ...         ...           ...     ...
        126   28067782  2014-10-24  2014-09-30      678820.0     TNL
        127   28067782  2015-02-10  2014-12-31      684470.0     TNL
        128   28067782  2015-04-28  2015-03-31      691327.0     TNL
        129   28067782  2015-07-28  2015-06-30      692592.0     TNL
        130   28067782  2015-10-27  2015-09-30      696018.0     TNL
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
        Usable data items for the hotel and gaming industry specific data component.

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
            >>> di = prism.industry.hotel.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                     dataitemname
            0      101990  Average Number of Slot Machines
            1      101991         Average Number of Tables
            2      101992        Casinos, Incl. JVs, Total
            3      101993                     Casinos, JVs
            4      101994   Gaming Space, Incl. JVs, Total
            ...       ...                              ...
            201    102191                     Rooms Closed
            202    102192                     Rooms Opened
            203    102193                       Rooms Sold
            204    102194               Rooms at Beginning
            205    102195                     Rooms, Total

            >>> di[["dataitemid", "dataitemname"]]
        """
        return cls._dataitems(search=search, package=package)


class insurance(_PrismIndustryFinancialDataComponent):
    """
    | Return the insurance industry specific data from financial statement.
    | Default frequency is quarterly.

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

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored. It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.industry.insurance.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid                                       dataitemname
        0        102196                      Investment in Debt Securities
        1        102197  Investment in Equity and Preferred Securities,...
        2        102198                           Trading Asset Securities
        3        102199                                  Real Estate Owned
        4        102200                                     Mortgage Loans
        ..          ...                                                ...
        448      102644                 Other Adjustment to Reserve at BOP
        449      102645                  L&H Statutory Capital and Surplus
        450      102646                   MC Statutory Capital and Surplus
        451      102647      Policy & Claims Statutory Capital and Surplus
        452      102648  Statutory Surplus (Statutory Capital and Surplus)

        >>> ind = prism.industry.insurnace(dataitemid=102200, periodtype='Q')
        >>> ind_df = ind.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ind_df
             listingid        date  currency      period  Mortgage Loans  Ticker
        0      2587390  2010-02-05       USD  2008-12-31    1.603400e+09     AET
        1      2587390  2010-04-29       USD  2010-03-31    1.457600e+09     AET
        2      2587390  2010-07-28       USD  2010-06-30    1.406300e+09     AET
        3      2587390  2010-11-03       USD  2010-09-30    1.423400e+09     AET
        4      2587390  2011-02-25       USD  2010-12-31    1.454600e+09     AET
        ..         ...         ...       ...         ...             ...     ...
        621   36842461  2010-04-23       USD  2010-03-31    3.900000e+07     TRV
        622   36842461  2011-01-25       USD  2010-12-31    3.400000e+07     TRV
        623   36842461  2012-01-24       USD  2011-12-31    3.600000e+07     TRV
        624   36842461  2012-04-19       USD  2012-03-31    3.600000e+07     TRV
        625   36842461  2013-01-22       USD  2012-12-31    4.000000e+06     TRV
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
        Usable data items for the insurance industry specific data component.

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
                - *dataitemid***
                - *datadescription*


        Examples
        --------
            >>> di = prism.industry.insurance.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                       dataitemname
            0      102196                      Investment in Debt Securities
            1      102197  Investment in Equity and Preferred Securities,...
            2      102198                           Trading Asset Securities
            3      102199                                  Real Estate Owned
            4      102200                                     Mortgage Loans
            ...       ...                                                ...
            448    102644                 Other Adjustment to Reserve at BOP
            449    102645                  L&H Statutory Capital and Surplus
            450    102646                   MC Statutory Capital and Surplus
            451    102647      Policy & Claims Statutory Capital and Surplus
            452    102648  Statutory Surplus (Statutory Capital and Surplus)
        """
        return cls._dataitems(search=search, package=package)


class internet(_PrismIndustryFinancialDataComponent):
    """
    | Return the internet industry specific data from financial statement.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.
            | This identifies the type of the balance sheet value (Revenue, Expense, etc.)

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
        >>> di = prism.industry.internet.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
           dataitemid                                     dataitemname
        0      102649                        Average Revenue Per Click
        1      102650               Change in Traffic Acquisition Cost
        2      102651                  Growth in Number of Paid Clicks
        3      102652                  Growth in Revenue Per Page View
        4      102653                             Number of Page Views
        5      102654                            Number of Paid Clicks
        6      102655                                Page Views Growth
        7      102656                         Traffic Acquisition Cost
        8      102657  Traffic Acquisition Cost to Adv. Revenues Ratio
        9      102658  Traffic Acquisition Cost to Total Revenue Ratio

        >>> ind = prism.industry.internet(dataitemid=102656, periodtype='Q')
        >>> ind_df = ind.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ind_df
            listingid        date  currency      period  Traffic Acquisition Cost  Ticker
        0     2665340  2010-01-26       USD  2009-12-31              4.735090e+08    LBTA
        1     2665340  2010-04-20       USD  2010-03-31              4.665300e+08    LBTA
        2     2665340  2010-07-20       USD  2010-06-30              4.732500e+08    LBTA
        3     2665340  2010-10-19       USD  2010-09-30              4.767840e+08    LBTA
        4     2665340  2011-01-25       USD  2010-12-31              3.198590e+08    LBTA
        ..        ...         ...       ...         ...                       ...     ...
        93  312940617  2015-02-09       USD  2014-12-31              3.620000e+09    GOOG
        94  312940617  2015-04-23       USD  2015-03-31              3.345000e+09    GOOG
        95  312940617  2015-04-29       USD  2015-03-31              3.345000e+09    GOOG
        96  312940617  2015-07-16       USD  2015-06-30              3.377000e+09    GOOG
        97  312940617  2015-07-23       USD  2015-06-30              3.377000e+09    GOOG
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
        Usable data items for the internet industry specific data component.

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
            >>> di = prism.industry.internet.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                     dataitemname
            0      102649                        Average Revenue Per Click
            1      102650               Change in Traffic Acquisition Cost
            2      102651                  Growth in Number of Paid Clicks
            3      102652                  Growth in Revenue Per Page View
            4      102653                             Number of Page Views
            5      102654                            Number of Paid Clicks
            6      102655                                Page Views Growth
            7      102656                         Traffic Acquisition Cost
            8      102657  Traffic Acquisition Cost to Adv. Revenues Ratio
            9      102658  Traffic Acquisition Cost to Total Revenue Ratio
        """
        return cls._dataitems(search=search, package=package)


class managed_care(_PrismIndustryFinancialDataComponent):
    """
    | Return the managed care industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.managed_care.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                             dataitemname
        0       102659                           Cash at Parent
        1       102660                          Claims Reserves
        2       102661                   Days in Claims Payable
        3       102662  Days in Claims Payable Excl. Capitation
        4       102663   Days of Unprocessed Claims Inventories
        ..         ...                                      ...
        62      102721                        Military Premiums
        63      102722                    Other Premiums, Total
        64      102723                       PPO / POS Premiums
        65      102724                Specialty ASO Fees, Total
        66      102725                Specialty Premiums, Total

        >>> ind = prism.industry.managed_care(dataitemid=102660, periodtype='Q')
        >>> ind_df = ind.get_data(universe="S&P 500", startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ind_df
             listingid        date      period  Claims Reserves  Ticker
        0      2586086  2010-02-02  2008-12-31     3.315000e+09     AFL
        1      2586086  2010-02-26  2009-12-31     3.270000e+09     AFL
        2      2586086  2010-04-27  2009-03-31     3.270000e+09     AFL
        3      2586086  2010-05-07  2010-03-31     3.298000e+09     AFL
        4      2586086  2010-07-27  2009-06-30     3.298000e+09     AFL
        ..         ...         ...         ...              ...     ...
        237   12867396  2015-01-28  2014-12-31     6.861200e+09    ANTM
        238   12867396  2015-02-24  2014-12-31     6.861200e+09    ANTM
        239   12867396  2015-04-29  2015-03-31     7.177100e+09    ANTM
        240   12867396  2015-07-29  2015-06-30     7.177900e+09    ANTM
        241   12867396  2015-10-28  2015-09-30     7.110100e+09    ANTM
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
        Usable data items for the managed care industry specific data component.

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
            >>> di = prism.industry.managed_care.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                             dataitemname
            0      102659                           Cash at Parent
            1      102660                          Claims Reserves
            2      102661                   Days in Claims Payable
            3      102662  Days in Claims Payable Excl. Capitation
            4      102663   Days of Unprocessed Claims Inventories
            ...       ...                                      ...
            62     102721                        Military Premiums
            63     102722                    Other Premiums, Total
            64     102723                       PPO / POS Premiums
            65     102724                Specialty ASO Fees, Total
            66     102725                Specialty Premiums, Total
        """
        return cls._dataitems(search=search, package=package)


class mining(_PrismIndustryFinancialDataComponent):
    """
    | Return the mining industry specific data from financial statement.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.
            | This identifies the type of the balance sheet value (Revenue, Expense, etc.)

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
        >>> di = prism.industry.mining.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid                                       dataitemname
        0        102739  Aluminium, Probable Attributable Ore Reserves (T)
        1        102740               Aluminium, Probable Ore Reserves (T)
        2        102741       Aluminium, Probable Recoverable Reserves (T)
        3        102742  Aluminium, Probable Recoverable and Attributab...
        4        102743                 Aluminium, Probable Reserves Grade
        ..          ...                                                ...
        231      102983	                             Gold, Number of Mines
        ..          ...                                                ...
        748      103629       Zinc, Measured and Indicated Resources Grade
        749      103630                     Zinc, Ore Resources (T), Total
        750      103631             Zinc, Recoverable Resources (T), Total
        751      103632  Zinc, Recoverable and Attributable Resources (...
        752      103633                       Zinc, Resources Grade, Total

        >>> ind = prism.industry.mining(dataitemid=102983, periodtype='A')
        >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
        >>> ind_df
            listingid        date  Gold, Number of Mines  Ticker
        0     2613632  2010-02-26                    9.0     FCX
        1     2613632  2011-02-25                    8.0     FCX
        2     2613632  2012-02-27                    8.0     FCX
        3     2615863  2011-02-23                    2.0     GSS
        4     2615863  2011-02-24                    2.0     GSS
        ..        ...         ...
        35   59434239  2010-02-25                    4.0     CDE
        36   59434239  2010-02-26                    3.0     CDE
        37   59434239  2011-02-28                    4.0     CDE
        38   59434239  2011-03-01                    4.0     CDE
        39   59434239  2012-02-23                    4.0     CDE
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
        Usable data items for the mining industry specific data component.


        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.mining.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                       dataitemname
            0      102739  Aluminium, Probable Attributable Ore Reserves (T)
            1      102740               Aluminium, Probable Ore Reserves (T)
            2      102741       Aluminium, Probable Recoverable Reserves (T)
            3      102742  Aluminium, Probable Recoverable and Attributab...
            4      102743                 Aluminium, Probable Reserves Grade
            ...       ...                                                ...
            748    103629       Zinc, Measured and Indicated Resources Grade
            749    103630                     Zinc, Ore Resources (T), Total
            750    103631             Zinc, Recoverable Resources (T), Total
            751    103632  Zinc, Recoverable and Attributable Resources (...
            752    103633                       Zinc, Resources Grade, Total
        """
        return cls._dataitems(search=search, package=package)


class oil(_PrismIndustryFinancialDataComponent):
    """
    | Return the oil and gas industry specific data from financial statement.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item.
            | This identifies the type of the balance sheet value (Revenue, Expense, etc.)

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
        >>> di = prism.industry.oil.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid                     dataitemname
        0        103634     Gross Developed (1000 acres)
        1        103635    Gross Developed (1000 sq. km)
        2        103636   Gross Undeveloped (1000 acres)
        3        103637  Gross Undeveloped (1000 sq. km)
        4        103638       Net Developed (1000 acres)
        ..          ...                              ...
        211      103845               Net Wells Drilling
        212      103846     Number of Rigs, Non-Operated
        213      103847         Number of Rigs, Operated
        214      103848            Number of Rigs, Total
        215      103849             Number of Wells, New

        >>> ind = prism.industry.oil(dataitemid=103848, periodtype='A')
        >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
        >>> ind_df
            listingid        date  Number of Rigs, Total  Ticker
        0     2586639  2011-03-16                    2.0    AXAS
        1     2586639  2012-03-15                    2.0    AXAS
        2     2594176  2010-02-25                    3.0     BRY
        3     2594176  2010-08-12                    3.0     BRY
        4     2594176  2011-03-01                    7.0     BRY
        ..        ...         ...                    ...     ...
        83  143970960  2012-10-09                   16.0     LPI
        84  143970960  2012-10-12                   16.0     LPI
        85  382989259  2011-03-16                    5.0  VTGD.F
        86  382989259  2011-05-02                    5.0  VTGD.F
        87  382989259  2012-03-15                    4.0  VTGD.F
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
        Usable data items for the oil and gas industry specific data component.

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
            >>> di = prism.industry.oil.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                     dataitemname
            0      103634     Gross Developed (1000 acres)
            1      103635    Gross Developed (1000 sq. km)
            2      103636   Gross Undeveloped (1000 acres)
            3      103637  Gross Undeveloped (1000 sq. km)
            4      103638       Net Developed (1000 acres)
            ...       ...                              ...
            211    103845               Net Wells Drilling
            212    103846     Number of Rigs, Non-Operated
            213    103847         Number of Rigs, Operated
            214    103848            Number of Rigs, Total
            215    103849             Number of Wells, New
        """
        return cls._dataitems(search=search, package=package)


class biopharma(_PrismIndustryFinancialDataComponent):
    """
    | Return the biotech and pharmaceutical industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.biopharma.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
              dataitemid	                                dataitemname
        0	      103850          Number of Licensed Patent Applications
        1	      103851                      Number of Licensed Patents
        2	      103852                   Number of Patent Applications
        3	      103853                               Number of Patents
        4	      103854   Number of Products Approved During the Period
        5	      103855   Number of Products Launched During the Period
        6	      103856      Number of Products in Clinical Development
        7	      103857        Number of Products in Discovery Research
        8	      103858                   Number of Products in Phase I
        9	      103859                  Number of Products in Phase II
        10        103860                 Number of Products in Phase III
        11        103861       Number of Products in Pre-Clinical Trials
        12        103862          Number of Products in Pre-Registration
        13        103863  Number of Products in Research and Development

        >>> ta = prism.industry.biopharma(dataitemid=103855, periodtype='Q')
        >>> ta_df = ta.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> ta_df
               listingid	    date	  period    Number of Products Launched During the Period    Ticker
        0	     2586533  2010-02-19  2008-12-31	                                          1.0	    ABT
        1	     2586533  2013-04-17  2013-03-31	                                         19.0	    ABT
        2	     2586533  2013-07-17  2013-06-30	                                         24.0	    ABT
        3	     2586533  2015-10-21  2015-09-30	                                          2.0	    ABT
        4	     2588113  2010-05-07  2010-03-31	                                          1.0	    AGN
        ...	         ...	     ...	     ...	                                          ...	    ...
        129	   244652395  2014-05-05  2013-09-30	                                          1.0	    ACT
        130	   244652395  2014-08-05  2013-09-30	                                          1.0	    ACT
        131	   244652395  2014-11-05  2013-09-30	                                          1.0	    ACT
        132	   253172906  2014-02-06  2013-03-31	                                          2.0	   PRGO
        133    253172906  2014-05-07  2014-03-31	                                         35.0	   PRGO
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
        Usable data items for the biotech and pharmaceutical industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.biopharma.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                    dataitemname
            0      103850          Number of Licensed Patent Applications
            1      103851                      Number of Licensed Patents
            2      103852                   Number of Patent Applications
            ...       ...                                             ...
            11     103861       Number of Products in Pre-Clinical Trials
            12     103862          Number of Products in Pre-Registration
            13     103863  Number of Products in Research and Development
        """
        return cls._dataitems(search=search, package=package)


class real_estate(_PrismIndustryFinancialDataComponent):
    """
    | Return the real estate industry specific data from financial statement.
    | Default frequency is quarterly.

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

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored. It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.industry.real_estate.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid                       dataitemname
        0        103864  Gross Property, Plant & Equipment
        1        103865  Land Held For Development or Sale
        2        103866           Accumulated Depreciation
        3        103867          Real Estate Assets, Total
        4        103868               Cash and Equivalents
        ..          ...                                ...
        437      104301    Consolidated Units, Undeveloped
        438      104302                      Managed Units
        439      104303                        Other Units
        440      104304               Unconsolidated Units
        441      104305                       Units, Total

        >>> ind = prism.industry.real_estate(dataitemid=104305, periodtype='A')
        >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
        >>> ind_df
             listingid        date  Units, Total  Ticker
        0      2589259  2010-03-31       11942.0     ARL
        1      2590254  2010-02-05      135654.0     AIV
        2      2590254  2010-02-26      135654.0     AIV
        3      2590254  2010-09-10      135654.0     AIV
        4      2590254  2011-02-04      122694.0     AIV
        ..         ...         ...           ...     ...
        180  114823500  2012-03-12        7606.0     CCG
        181  115561909  2012-09-13         773.0    SBRA
        182  115561909  2012-10-12         773.0    SBRA
        183  117844806  2012-03-06         922.0     AAT
        184  117844806  2012-03-09         922.0     AAT
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
        Usable data items for the real estate industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.real_estate_dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                       dataitemname
            0      103864  Gross Property, Plant & Equipment
            1      103865  Land Held For Development or Sale
            2      103866           Accumulated Depreciation
            3      103867          Real Estate Assets, Total
            4      103868               Cash and Equivalents
            ...       ...                                ...
            437    104301    Consolidated Units, Undeveloped
            438    104302                      Managed Units
            439    104303                        Other Units
            440    104304               Unconsolidated Units
            441    104305                       Units, Total
        """
        return cls._dataitems(search=search, package=package)


class restaurant(_PrismIndustryFinancialDataComponent):
    """
    | Return the restaurant industry specific data from financial statement.
    | Default frequency is quarterly.

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
        Usable data items for the restaurant industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.restaurant.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                    dataitemname
            0      104306       Affiliated and Other Restaurants Acquired
            1      104307         Affiliated and Other Restaurants Closed
            2      104308         Affiliated and Other Restaurants Opened
            3      104309           Affiliated and Other Restaurants Sold
            4      104310   Affiliated and Other Restaurants at Beginning
            ...       ...                                             ...
            33     104339         Owned / Operated Same Restaurants Sales
            34     104340  Owned / Operated Same Restaurants Sales Growth
            35     104341            Same Restaurants Sales Growth, Total
            36     104342                   Same Restaurants Sales, Total
        """
        return cls._dataitems(search=search, package=package)


class retail(_PrismIndustryFinancialDataComponent):
    """
    | Return the retail industry specific data from financial statement.
    | Default frequency is quarterly.

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

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored. It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.industry.retail.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                              dataitemname
        0       104343      Affiliated and Other Stores Acquired
        1       104344        Affiliated and Other Stores Closed
        2       104345        Affiliated and Other Stores Opened
        3       104346          Affiliated and Other Stores Sold
        4       104347  Affiliated and Other Stores at Beginning
        ..         ...                                       ...
        57      104400                             Stores Opened
        58      104401                               Stores Sold
        59      104402                       Stores at Beginning
        60      104403                             Stores, Total
        61      104404                        Wholesale Revenues

        >>> ind = prism.industry.retail(dataitemid=104403, periodtype='A')
        >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
        >>> ind_df
             listingid        date  Stores, Total  Ticker
        0      2586503  2010-02-16         1694.0     RNT
        1      2586503  2010-02-26         1694.0     RNT
        2      2586505  2011-02-16         1814.0     AAN
        3      2586505  2011-02-25         1814.0     AAN
        4      2586505  2012-02-09         1945.0     AAN
        ..         ...         ...            ...     ...
        942  324468442  2011-03-09         1192.0      MW
        943  324468442  2011-03-30         1192.0      MW
        944  324468442  2012-03-07         1166.0      MW
        945  324468442  2012-03-28         1166.0      MW
        946  324743938  2011-02-10           17.0    INNO
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
        Usable data items for the retail industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.retail.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                              dataitemname
            0      104343      Affiliated and Other Stores Acquired
            1      104344        Affiliated and Other Stores Closed
            2      104345        Affiliated and Other Stores Opened
            3      104346          Affiliated and Other Stores Sold
            4      104347  Affiliated and Other Stores at Beginning
            ...       ...                                       ...
            57     104400                             Stores Opened
            58     104401                               Stores Sold
            59     104402                       Stores at Beginning
            60     104403                             Stores, Total
            61     104404                        Wholesale Revenues
        """
        return cls._dataitems(search=search, package=package)


class semiconductors(_PrismIndustryFinancialDataComponent):
    """
    | Return the semiconductor industry specific data from financial statement.
    | Default frequency is quarterly.

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
        >>> di = prism.industry.semiconductors.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
            dataitemid                    dataitemname
        0       104405    Average Price Per Back Order
        1       104406         Average Price Per Order
        2       104407                   Backlog Value
        3       104408              Book to Bill Ratio
        4       104409           Change in Order Value
        5       104410        Number of Backlog Orders
        6       104411                Number of Orders
        7       104412                     Order Value
        8       104413               Warranty Reserves
        9       104414      Warranty Reserves Acquired
        10      104415        Warranty Reserves Issued
        11      104416   Warranty Reserves Other Items
        12      104417      Warranty Reserves Payments
        13      104418  Warranty Reserves at Beginning

        >>> ind = prism.industry.semiconductors(dataitemid=104403, periodtype='A')
        >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
        >>> ind_df
             listingid  currency        date  Backlog Value  Ticker
        0      2586858       USD  2010-03-15   6.420000e+07    ACTL
        1      2587347       USD  2010-02-16   6.620000e+07    AEIS
        2      2587347       USD  2010-02-26   6.600000e+07    AEIS
        3      2587347       USD  2011-03-02   9.310000e+07    AEIS
        4      2587347       USD  2012-03-02   7.690000e+07    AEIS
        ..         ...       ...         ...            ...     ...
        155   99345549       USD  2011-07-28   1.100000e+09     FSL
        156   99345549       USD  2012-02-03   8.440000e+08     FSL
        157  117909280       USD  2012-06-19   1.710000e+07    INVN
        158  142650520       USD  2012-02-07   8.560000e+07     IMI
        159  142650520       USD  2012-03-16   8.560000e+07     IMI
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
        Usable data items for the semiconductor industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.semiconductors.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                    dataitemname
            0      104405    Average Price Per Back Order
            1      104406         Average Price Per Order
            2      104407                   Backlog Value
            3      104408              Book to Bill Ratio
            ...       ...                             ...
            10     104415        Warranty Reserves Issued
            11     104416   Warranty Reserves Other Items
            12     104417      Warranty Reserves Payments
            13     104418  Warranty Reserves at Beginning
        """
        return cls._dataitems(search=search, package=package)


class telecom(_PrismIndustryFinancialDataComponent):
    """
    | Return the telecom industry specific data from financial statement.
    | Default frequency is quarterly.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        periodtype : str, {'A', 'Annual', 'SA', 'Semi-Annual', 'Quarterly', 'Q', 'LTM', 'YTD'}
            | Financial Period in which the financial statement results are reported.*
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

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored. It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
    >>> di = prism.industry.telecom.dataitems()
    >>> di[['dataitemid', 'dataitemname']]
         dataitemid                               dataitemname
    0        104419                      Minutes of Use, Local
    1        104420              Minutes of Use, Long Distance
    2        104421                          Basic Penetration
    3        104422                      Broadband Penetration
    4        104423           Broadband Penetration (% of THP)
    ..          ...                                        ...
    107      104526               Prepaid Wireless Subscribers
    108      104527  Reseller / Wholesale Wireless Subscribers
    109      104528   Roaming Minutes of Use by Other Carriers
    110      104529                       Wireless Penetration
    111      104530                Wireless Subscribers, Total

    >>> ind = prism.industry.semiconductors(dataitemid=104530, periodtype='A')
    >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
    >>> ind_df
         listingid        date  Wireless Subscribers, Total  Ticker
    0      2587788  2010-03-04                     137365.0    ALSK
    1      2587788  2010-03-09                     137365.0    ALSK
    2      2587788  2011-02-24                     120413.0    ALSK
    3      2587788  2011-02-28                     120413.0    ALSK
    4      2587788  2012-03-01                     117559.0    ALSK
    ..         ...         ...                          ...     ...
    98    33965372  2012-02-23                    9346659.0     PCS
    99    33965372  2012-02-29                    9346659.0     PCS
    100   70011082  2011-03-07                     426900.0    IRDM
    101   70011082  2012-03-06                     522600.0    IRDM
    102   70011082  2012-11-20                     522600.0    IRDM
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
        Usable data items for the telecom industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.telecom.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                               dataitemname
            0      104419                      Minutes of Use, Local
            1      104420              Minutes of Use, Long Distance
            2      104421                          Basic Penetration
            3      104422                      Broadband Penetration
            4      104423           Broadband Penetration (% of THP)
            ...       ...                                        ...
            107    104526               Prepaid Wireless Subscribers
            108    104527  Reseller / Wholesale Wireless Subscribers
            109    104528   Roaming Minutes of Use by Other Carriers
            110    104529                       Wireless Penetration
            111    104530                Wireless Subscribers, Total
        """
        return cls._dataitems(search=search, package=package)


class utility(_PrismIndustryFinancialDataComponent):
    """
    | Utility industry specific data from financial statement.
    | Default frequency is quarterly.

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

                | If a selected data item is not a currency value (i.e airplanes owned), the currency input will be ignored. It will behave like parameter input currency=None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.industry.utility.dataitems()
        >>> di[['dataitemid', 'dataitemname']]
             dataitemid                             dataitemname
        0        104531                     Cash and Equivalents
        1        104532                   Short-Term Investments
        2        104533                 Trading Asset Securities
        3        104534                      Accounts Receivable
        4        104535                        Other Receivables
        ..          ...                                      ...
        193      104724        Other Preferred Stock Adjustments
        194      104725          Other Adjustments to Net Income
        195      104726  Net Income Allocable to General Partner
        196      104727   Net Income to Common Incl. Extra Items
        197      104728   Net Income to Common Excl. Extra Items

        >>> ind = prism.industry.utility(dataitemid=104531, periodtype='A')
        >>> ind_df = ind.get_data(universe="Russell 3000", startdate='2010-01-01', enddate='2012-12-31', shownid=['ticker'])
        >>> ind_df
               listingid  currency        date  Cash and Equivalents  Ticker
        0        2585893       USD  2010-03-15            25639000.0    AAON
        1        2585893       USD  2011-03-10             2393000.0    AAON
        2        2585893       USD  2012-03-14               13000.0    AAON
        3        2585895       USD  2010-07-13            79370000.0     AIR
        4        2585895       USD  2010-07-16            79370000.0     AIR
        ...          ...       ...         ...                   ...     ...
        17006  578353660       USD  2010-09-08           654396000.0  GGWP.Q
        17007  578353660       USD  2010-10-15           654396000.0  GGWP.Q
        17008  578353660       USD  2010-11-01           654396000.0  GGWP.Q
        17009  578353660       USD  2010-11-03           654396000.0  GGWP.Q
        17010  578353660       USD  2010-11-09           654396000.0  GGWP.Q
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
        Usable data items for the utility industry specific data component.

        Parameters
        ----------
            search : str, default None
                Search word for dataitems name, the search is case-insensitive.

            package : str, default None
                Search word for package name, the search is case-insensitive.

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
            >>> di = prism.industry.utility.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                             dataitemname
            0      104531                     Cash and Equivalents
            1      104532                   Short-Term Investments
            2      104533                 Trading Asset Securities
            3      104534                      Accounts Receivable
            4      104535                        Other Receivables
            ...       ...                                      ...
            193    104724        Other Preferred Stock Adjustments
            194    104725          Other Adjustments to Net Income
            195    104726  Net Income Allocable to General Partner
            196    104727   Net Income to Common Incl. Extra Items
            197    104728   Net Income to Common Excl. Extra Items
        """
        return cls._dataitems(search=search, package=package)


@_validate_args
def dataitems(search: str = None, package: str = None):
    """
    Usable data items for the industry data category.

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
        >>> di = prism.industry.dataitems()
        >>> di[["dataitemid", "dataitemname"]]
              dataitemid                             dataitemname
        0         100916             Aircraft Average Age (Years)
        1         100917                          Aircraft Leased
        2         100918                  Aircraft Not in Service
        3         100919                           Aircraft Owned
        4         100920         Aircraft Retired during the Year
        ...          ...                                      ...
        3653      104724        Other Preferred Stock Adjustments
        3654      104725          Other Adjustments to Net Income
        3655      104726  Net Income Allocable to General Partner
        3656      104727   Net Income to Common Incl. Extra Items
        3657      104728   Net Income to Common Excl. Extra Items
    """

    return _list_dataitem(
        datacategoryid=_PrismIndustryFinancialDataComponent.categoryid,
        datacomponentid=None,
        search=search,
        package=package,
    )
