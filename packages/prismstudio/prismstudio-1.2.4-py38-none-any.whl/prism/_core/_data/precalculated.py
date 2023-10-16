from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from .._req_builder import _list_dataitem
from ..._utils import _validate_args

__all__ = ['alpha_factor_library', 'dataitems']


_data_category = __name__.split(".")[-1]


@_validate_args
class alpha_factor_library(_PrismComponent, _PrismDataComponent):
    """
    | Pre-calculated factor dataset provided by S&P Global Market Intelligence.
    | Default frequency is quarterly.


    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.precalculated.afl.dataitems('Turnover')
        >>> di[['dataitemid', 'dataitemname']]
           dataitemid                                  dataitemname
        0      900075                      1Y Chg in Sales Turnover
        1      900078                      1Y Chg in Share Turnover
        2      900114                      3Y Chg in Sales Turnover
        3      900158      5 Yr Hist Rel Receivables Turnover Ratio
        4	   900168  5 Yr Hist Rel Working Capital Turnover Ratio
        5      900225                                Asset Turnover
        6      900226                             Asset Turnover v2
        7      900261                      Change of Asset Turnover
        8      900262                   Change of Asset Turnover v2
        9      900306                               Equity Turnover
        10     900352                    Ind Grp Rel Asset Turnover
        11     900384                Ind Grp Rel Inventory Turnover
        12     900404        Ind Grp Rel Receivables Turnover Ratio
        13     900420    Ind Grp Rel Working Capital Turnover Ratio
        14     900431                Institution Ownership Turnover
        15     900434                            Inventory Turnover
        16     900525                    Receivables Turnover Ratio
        17     900568                                Share Turnover
        18     900636                Working Capital Turnover Ratio

        >>> turnover = prism.precalculated.alpha_factor_library(dataitemid=900306)
        >>> turnover_df = turnover.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> turnover_df
              listingid        date  Equity Turnover  Ticker
        0       2586086  2010-01-31          2.74645     AFL
        1       2586086  2010-02-28          2.61951     AFL
        2       2586086  2010-03-31          2.61951     AFL
        3       2586086  2010-04-30          2.33898     AFL
        4       2586086  2010-05-31          2.33898     AFL
          ...         ...         ...              ...     ...
        36623  344286611  2011-06-30          2.53677    ITT
        36624  344286611  2011-07-31          2.46787    ITT
        36625  344286611  2011-08-31          2.46787    ITT
        36626  344286611  2011-09-30          2.46787    ITT
        36627  344286611  2011-10-31          2.55218    ITT
    """

    _component_category_repr = _data_category

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None):
        """
        Usable data items for the alpha factor library datacomponent.

        Parameters
        ----------
            search : str, default None
                | Search word for dataitems name, the search is case-insensitive.

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
            >>> di = prism.precalculated.afl.dataitems("Debt")
            >>> di[['dataitemid', 'dataitemname']]
            dataitemid                                       dataitemname
            0      900033  1-Year Change in Long Term Debt to Avg Total A...
            1      900059                           1Y Chg in Debt to Assets
            2      900145       5 Yr Hist Rel Long Term Debt to Assets Ratio
            3      900279                               Debt to Assets Ratio
            4      900366                   Ind Grp Rel Debt to Assets Ratio
            5      900388         Ind Grp Rel Long Term Debt to Assets Ratio
            6      900389         Ind Grp Rel Long Term Debt to Equity Ratio
            7      900425    Ind Grp Rel Year over Year Change of Total Debt
            8      900451                     Long Term Debt to Assets Ratio
            9      900452                     Long Term Debt to Equity Ratio
            10     900644                Year over Year Change of Total Debt
        """
        return _list_dataitem(
            datacategoryid=cls.categoryid,
            datacomponentid=cls.componentid,
            search=search,
            package=None,
        )


def dataitems(search: str = None):
    """
    Usable data items for the precalculated data category.

    Parameters
    ----------
        search : str, default None
            | Search word for dataitems name, the search is case-insensitive.

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
        >>> di = prism.precalculated.dataitems("Debt")
        >>> di[['dataitemid', 'dataitemname']]
           dataitemid                                       dataitemname
        0      900033  1-Year Change in Long Term Debt to Avg Total A...
        1      900059                           1Y Chg in Debt to Assets
        2      900145       5 Yr Hist Rel Long Term Debt to Assets Ratio
        3      900279                               Debt to Assets Ratio
        4      900366                   Ind Grp Rel Debt to Assets Ratio
        5      900388         Ind Grp Rel Long Term Debt to Assets Ratio
        6      900389         Ind Grp Rel Long Term Debt to Equity Ratio
        7      900425    Ind Grp Rel Year over Year Change of Total Debt
        8      900451                     Long Term Debt to Assets Ratio
        9      900452                     Long Term Debt to Equity Ratio
        10     900644                Year over Year Change of Total Debt
    """
    return _list_dataitem(
        datacategoryid=alpha_factor_library.categoryid,
        datacomponentid=None,
        search=search,
        package=None,
    )
