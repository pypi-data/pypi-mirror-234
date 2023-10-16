from .._req_builder import _list_dataitem
from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from ..._utils import _validate_args, _get_params
from ..._common import const

__all__ = ['news', 'earnings_call', 'dataitems', 'news_dataitems']


_data_category = __name__.split(".")[-1]


class _PrismEventComponent(_PrismDataComponent):
    _component_category_repr = _data_category

    @classmethod
    def _dataitems(cls, search: str = None, package: str = None):
        return _list_dataitem(
            datacategoryid=cls.categoryid,
            datacomponentid=cls.componentid,
            search=search,
            package=package,
        )


class news(_PrismEventComponent):
    """
    | News data for a specific event type.
    | Default frequency is aperiodic.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

        datetype : str, {'entereddate', 'announceddate'}, default 'entereddate'
            | Datetype determines which date is fetched.

            - entereddate: when news data is inserted to the database
            - announceddate: when news data is announced

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.event.dataitems()
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid                                  dataitemname
        0      400001                               Address Changes
        1      400002                          Analyst/Investor Day
        2      400003  Announcement of Interim Management Statement
        3      400004             Announcement of Operating Results
        4      400005                     Announcements of Earnings
        ...       ...                                           ...
        156    400157                         Stock Dividends (<5%)
        157    400158    Stock Splits & Significant Stock Dividends
        158    400159                           Strategic Alliances
        159    400160                 Structured Products Offerings
        160    400161                                Ticker Changes

        >>> news = prism.event.news(dataitemid=400005)
        >>> news_df = news.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2015-12-31", shownid=["Company Name"])
        >>> news_df
               listingid                 date                                           headline                                            content                 Company Name
        0        2588294  2010-04-28 22:51:00  The Allstate Corporation Reports Earnings Resu...  The Allstate Corporation reported earnings res...                ALLSTATE CORP
        1        2588294  2010-02-11 00:55:00  Allstate Corp. Reports Earnings Results for th...  Allstate Corp. reported earnings results for t...                ALLSTATE CORP
        2        2588294  2010-04-28 22:40:00  The Allstate Corporation Reports Earnings Resu...  The Allstate Corporation reported earnings res...                ALLSTATE CORP
        3        2588294  2010-10-27 23:36:00  The Allstate Corporation Reports Unaudited Con...  The Allstate Corporation reported unaudited co...                ALLSTATE CORP
        4        2588294  2011-08-02 00:09:00  Allstate Corp. Reports Earnings Results for th...  Allstate Corp. reported earnings results for t...                ALLSTATE CORP
        ...          ...                  ...                                                ...                                                ...                          ...
        13056  302980253  2015-10-20 00:03:00  NiSource Gas Transmission & Storage Company Re...  NiSource Gas Transmission & Storage Company re...  COLUMBIA PIPELINE GROUP INC
        13057  302980253  2015-10-20 00:03:00  NiSource Gas Transmission & Storage Company An...  NiSource Gas Transmission & Storage Company an...  COLUMBIA PIPELINE GROUP INC
        13058  302980253  2015-10-20 00:03:00  NiSource Gas Transmission & Storage Company Re...  NiSource Gas Transmission & Storage Company re...  COLUMBIA PIPELINE GROUP INC
        13059  302980253  2015-11-03 07:42:00  Columbia Pipeline Group, Inc. Announces Unaudi...  Columbia Pipeline Group, Inc. announced unaudi...  COLUMBIA PIPELINE GROUP INC
        13060  316754620  2015-12-02 21:26:00  Computer Sciences GS Business Reports Unaudite...  Computer Sciences GS Business reported unaudit...                     CSRA INC
    """
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        datetype: const.DateType = 'entereddate',
        package: str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search: str = None, package: str = None):
        """
        Usable data items for the news data component.

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
            >>> di = prism.event.news.dataitems()
            >>> di[["dataitemid", "dataitemname"]]
            dataitemid                                  dataitemname
            0      400001                               Address Changes
            1      400002                          Analyst/Investor Day
            2      400003  Announcement of Interim Management Statement
            3      400004             Announcement of Operating Results
            4      400005                     Announcements of Earnings
            ...       ...                                           ...
            156    400157                         Stock Dividends (<5%)
            157    400158    Stock Splits & Significant Stock Dividends
            158    400159                           Strategic Alliances
            159    400160                 Structured Products Offerings
            160    400161                                Ticker Changes
        """
        return cls._dataitems(search=search, package=package)


class earnings_call(_PrismEventComponent):
    @_validate_args
    def __init__(self, package: str = None):
        super().__init__(**_get_params(vars()))


def dataitems(search: str = None, package: str = None):
    """
    Usable data items for the event data category.

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
        >>> di = prism.event.dataitems()
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid                                  dataitemname
        0      400001                               Address Changes
        1      400002                          Analyst/Investor Day
        2      400003  Announcement of Interim Management Statement
        3      400004             Announcement of Operating Results
        4      400005                     Announcements of Earnings
        ...       ...                                           ...
        156    400157                         Stock Dividends (<5%)
        157    400158    Stock Splits & Significant Stock Dividends
        158    400159                           Strategic Alliances
        159    400160                 Structured Products Offerings
        160    400161                                Ticker Changes
    """
    return _list_dataitem(
        datacategoryid=_PrismEventComponent.categoryid,
        datacomponentid=None,
        search=search,
        package=package,
    )
