import requests
import webbrowser
import warnings
from typing import List, Union

import pandas as pd

from ..._common.config import *
from ..._common.const import *
from ..._core._req_builder._universe import parse_universe_to_universeid
from ..._core._req_builder._portfolio import parse_portfolios_to_portfolioids
from ..._utils import (
    _authentication,
    get,
    _process_fileresponse,
    _validate_args,
    _get_web_authentication_token,
    are_periods_exclusive,
    get_sm_attributevalue,
)
from ..._utils.exceptions import PrismValueError, PrismTypeError
from ..._prismcomponent import prismcomponent as pcmpt, taskcomponent
from ..._prismcomponent import abstract_prismcomponent


__all__ = [
    "screen",
    "export_data",
    "factor_backtest",
    "get_factor_backtest_result",
]


@_validate_args
def screen(
    rule: abstract_prismcomponent._AbstractPrismComponent,
    universe: Union[int, str],
    frequency: str,
    startdate: str = None,
    enddate: str = None,
):
    """
    Returns screen task component which enables users to quickly construct custom time-variant universes through user defined rules to evaluate over the specified startdate and enddate.

    Parameters
    ----------
        rule: prism._PrismComponent
            | Boolean datatyped PrismComponent that the user defines rules to determine which issues pass the screen and which issues are filtered out.

        universe: str
            | Universe in which screen to be performed on

        frequency: str, {'D', 'BD', 'W', 'BM', 'M', 'Q', 'A'}
            | Desired rebalancing frequency to run screen.

        startdate: str, default None
            | Startdate of the time period for which to load data or the window in time in which to run a task.
            | If None, startdate of the universe will be used.

        enddate: str, default None
            | Enddate of the time period for which to load data or the window in time in which to run a task.
            | If None, enddate of the universe will be used.

    Returns
    -------
        Screen component: prism._Screen
            Prism Screen Task Component.

    Examples
    --------
        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31

        >>> mcap = prism.market.market_cap()
        >>> marketcap_rule = mcap.cross_sectional_rank() <= 200 # Top 200 market capitalization
        >>> snp_200_screen = prism.screen(
                rule=marketcap_rule,
                universe="S&P 500",
                startdate="2010-01-01",
                enddate="2015-01-01",
                frequency="D",
                )
        >>> snp_200_screen.run(newuniversename="snp_200")
        {'status': 'Pending',
        'message': 'screen pending',
        'result': [{'resulttype': 'jobid', 'resultvalue': 5}]}

        >>> prism.job_manager()
        >>> # Wait for job 5 in GUI until its status changed to 'Completed'

        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31
        4           5                      snp_200         index  2010-01-01  2015-01-01
    """
    if isinstance(rule, pcmpt._PrismDataComponent) or FUNCTIONS.get(rule._component_name)["type"] != "logical":
        raise PrismTypeError("screen task only available to boolean operations.")
    universeid, _ = parse_universe_to_universeid(universe)

    universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
    universe_startdate = universe_info["Start Date"].values[0]
    universe_enddate = universe_info["End Date"].values[0]

    universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

    if universe_period_violated:
        raise PrismValueError(
            f'Screen period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
        )

    return taskcomponent._Screen(
        rule_dataquery=[rule._query],
        universeid=int(universeid),
        frequency=frequency,
        startdate=startdate,
        enddate=enddate,
    )

@_validate_args
def export_data(
    component: Union[abstract_prismcomponent._AbstractPrismComponent, list],
    universe: Union[str, int] = None,
    startdate: str = None,
    enddate: str = None,
    shownid: list = None,
    display_pit: bool = True,
    name: Union[str, list] = None,
):
    """
    Returns export_data task component which enables users to quickly retrieve and save data of the specified components.

    Parameters
    ----------
        component : PrismComponent or list
            | PrismComponent which hold the logic to query data.

        universe:
            | Universe name (*str*) or universe id (*int*) used to query data.
            | Some components do not require universe information (eg. Exchange Rate), in which case to be left None.

        startdate : str, default None
            | Start date of the data. The data includes start date.
            | If None, the start date of the universe is used. The same applies when the input is earlier than the universe start date.

        enddate : str, default None
            | End date of the data. The data excludes end date.
            | If None, the end date of the universe is used. The same applies when the input is later than the universe end date.

        shownid : list, default None
            | List of Security Master attributes to display with the data.
            | See prism securitymaster list_attribute for full list of Security Master attributes.
            | If None, default attributes set in preferences is shown.
            | If empty list ([]), no attribute is shown.

        display_pit: bool, default True
            | If True, universe data is left-joined to show missing (NA) values.
            | If False, the NA values are dropped.

        name : str or list, default None
            | Column names of the data to display.
            | If one component is passed to the function, accepts either string or list with one element.
            | If multiple components is passed to the function, accepts list of string.
            | If None:

            - If data component is passed, the column name is implicitly decided following the name of the data component.
            - If function component is passed, the default column name is 'value'.

    Returns
    -------
        ExportData component: prism._ExportData
            Prism Export Data Task Component.

    Examples
    --------
        >>> close = prism.market.close()
        >>> open = prism.market.open()
        >>> ed = prism.export_data([close, open], "KRX_300", "2022-01-01")
        ==== TaskComponentType.EXPORT_DATA
            Query Structure
        >>> ed.run("filepath/close", ["close", "open"])
        export_data is added to worker queue!
        {'status': 'Pending',
        'message': 'export_data is added to worker queue!',
        'result': [{'resulttype': 'jobid', 'resultvalue': 465}]}

    """
    query = []
    cmpts = set()
    if isinstance(name, list) & (name is not None):
        if any([not isinstance(n, str) for n in name]):
            raise PrismTypeError('Names shoud be string')

    def add_cmpts(o):
        cmpts = set()
        if o["component_type"] == "datacomponent":
            cmpts.add(o["component_name"])
        else:
            for c in o["children"]:
                cmpts = cmpts | add_cmpts(c)
        return cmpts

    if not isinstance(component, list):
        component = [component]
    for o in component:
        if isinstance(o, abstract_prismcomponent._AbstractPrismComponent):
            query.append(o._query)
            cmpts = add_cmpts(o._query)
        else:
            raise PrismTypeError(f"Please provide Components into export_data")

    if len(cmpts - set(UniverseFreeDataComponentType)) == 0:
        universeid = None
    else:
        universeid, _ = parse_universe_to_universeid(universe)

    universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
    universe_startdate = universe_info["Start Date"].values[0]
    universe_enddate = universe_info["End Date"].values[0]

    universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

    if universe_period_violated:
        raise PrismValueError(
            f'Query period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
        )

    default_shownid = True
    if (shownid is not None) and (len(shownid) == 0):
        shownid = None
        default_shownid = False
    if shownid is not None:
        shownid = [get_sm_attributevalue(a) for a in shownid]
    component_names = set([c._component_name for c in component])
    if (len(component_names - set(AggregateComponents)) == 0) & (shownid is not None):
        warnings.warn(f"Shownid will be ignored for: {list(component_names & set(AggregateComponents))}")


    return taskcomponent._ExportData(
        dataqueries=query,
        universeid=int(universeid),
        startdate=startdate,
        enddate=enddate,
        shownid=shownid,
        default_shownid=default_shownid,
        datanames=name,
        display_pit=display_pit,
    )


@_validate_args
def factor_backtest(
    factor: Union[abstract_prismcomponent._AbstractPrismComponent, pd.DataFrame],
    universe: Union[int, str],
    frequency: str,
    bins: int,
    startdate: str = None,
    enddate: str = None,
    max_days: int = None,
    rank_method: str = "standard",
):
    """
    Return Factor Backtest task component which enables users to quickly test and identify factors which may predict future return.

    Parameters
    ----------
        factor: prism._PrismComponent
            | Specify which factor you want to run as part of the factor backtest.

        universe: str
            | Universe in which factor backtest to be performed on.

        frequency: str, {'D', 'BD', 'W', 'BM', 'M', 'Q', 'A'}
            | Desired rebalancing frequency for the factor_backtest.

        bins: int
            | Number of quantile portfolio the universe generate. Should be bigger than 1 and smaller than or equal to 20.

            .. admonition:: Warning
                :class: warning

                Bins are assigned to the factor score in descending order. Meaning the largest factor score will be assigned 1st bin

        startdate: str, default None
            | Startdate of the time period for which to load data or the window in time in which to run a task.
            | If None, startdate of the universe will be used.

        enddate: str, default None
            | Enddate of the time period for which to load data or the window in time in which to run a task.
            | If None, enddate of the universe will be used.

        max_days: int, default None
            | If None, default max days is induced from rebalancing frequency.

        rank_method: str, {'standard', 'modified', 'dense', 'ordinal', 'fractional'}, default 'standard'
            | Method for how equal values are assigned a rank.

            - standard : 1 2 2 4
            - modified : 1 3 3 4
            - dense : 1 2 2 3
            - ordinal : 1 2 3 4
            - fractional : 1 2.5 2.5 4

    Returns
    -------
        Factor Backtest component: prism._FactorBacktest
            Prism Factor Backtest Task Component.

    Examples
    --------
        >>> ni = prism.financial.income_statement(dataitemid=100639, periodtype='LTM')
        >>> mcap = prism.market.market_cap()
        >>> ep = ni / mcap
        >>> fb_ep = prism.factor_backtest(
                factor=ep,
                universe='Russell 3000 Index',
                frequency='Q',
                bins=5,
                startdate='2010-01-01',
                enddate='2015-01-01'
                )
        >>> fb_price_mom.run()
        factor_backtest is added to worker queue!: jobid is 1

        >>> prism.job_manager()
        >>> # Wait for the job 1 in GUI until its status changed to 'Completed'

        >>> prism.get_factor_backtest_result(1)
        Done!
        factor_backtest Completed: factorbacktestid is 1
        Fetching A Link to Factor Backtest Report...
        Link to Factor Backtest Report:
        https://ext.prism39.com/report/factor_backtest/my_username_1_afc7730c-55e6-41a8-ad4f-77df20caecc9/

        .. image:: ../../_static/factorbacktest-screenshot.png

    """
    if (bins < 2) or (bins > 20):
        PrismValueError("The number of bins should be between 2 and 20")

    if not isinstance(factor, list):
        factor = [factor]
    factor_ = []
    for f in factor:
        if isinstance(f, pd.DataFrame):
            if len(set(f.columns) & {"date", "listingid", "value"}) != 3:
                raise PrismValueError("Columns should be: date, listingid, value")
            if f.empty:
                raise PrismValueError("Dataframe should not be empty")
            factor_.append(f)
        elif isinstance(f, abstract_prismcomponent._AbstractPrismComponent):
            factor_.append(f._query)
        else:
            raise PrismValueError("Factor should be either prism component or a pandas dataframe")

    universeid, _ = parse_universe_to_universeid(universe)

    universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
    universe_startdate = universe_info["Start Date"].values[0]
    universe_enddate = universe_info["End Date"].values[0]

    universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

    if universe_period_violated:
        raise PrismValueError(
            f'Factor Backtest period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
        )

    return taskcomponent._FactorBacktest(
        factor_dataquery=factor_,
        universeid=int(universeid),
        frequency=frequency,
        bins=bins,
        rank_method=rank_method,
        max_days=max_days,
        startdate=startdate,
        enddate=enddate,
    )


@_validate_args
def strategy_backtest(
    trade: abstract_prismcomponent._AbstractPrismComponent,
    universe: Union[int, str],
    market_impact: str,
    commission_fee: str,
    short_loan_fee: str,
    risk_free_rate: str,
    margin_rate: str,
    cash_interest_rate: str,
    initial_position_type: str,
    initial_position_value: int,
    benchmark: List[Union[int, str]],
    currency: str,
    market_impact_value: float = None,
    commission_fee_value: float = None,
    short_loan_fee_value: float = None,
    risk_free_rate_value: float = None,
    margin_rate_value: float = None,
    cash_interest_rate_value: float = None,
    currency_hedge: bool = False,
    startdate: str = None,
    enddate: str = None,
    unpaid_dividend=None,
):
    assert initial_position_type in ["cash", "portfolio"], "Initial Position Type should be one of: cash, portfolio"
    if not isinstance(benchmark, list):
        benchmark = [benchmark]
    benchmark = parse_portfolios_to_portfolioids(benchmark)
    universeid, _ = parse_universe_to_universeid(universe)

    universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
    universe_startdate = universe_info["Start Date"].values[0]
    universe_enddate = universe_info["End Date"].values[0]

    universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

    if universe_period_violated:
        raise PrismValueError(
            f'Strategy Backtest period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
        )

    return taskcomponent._StrategyBacktest(
        trade_dataquery=trade._query,
        universeid=int(universeid),
        market_impact=market_impact,
        market_impact_value=market_impact_value,
        commission_fee=commission_fee,
        commission_fee_value=commission_fee_value,
        short_loan_fee=short_loan_fee,
        short_loan_fee_value=short_loan_fee_value,
        risk_free_rate=risk_free_rate,
        risk_free_rate_value=risk_free_rate_value,
        margin_rate=margin_rate,
        margin_rate_value=margin_rate_value,
        cash_interest_rate=cash_interest_rate,
        cash_interest_rate_value=cash_interest_rate_value,
        initial_position_type=initial_position_type,
        initial_position_value=initial_position_value,
        benchmark=benchmark,
        currency=currency,
        currency_hedge=currency_hedge,
        startdate=startdate,
        enddate=enddate,
        unpaid_dividend=unpaid_dividend,
    )


def get_factor_backtest_result(fbid: Union[list, int], data=True, report=False):
    """
    Return factor backtested result.

    Parameters
    ----------
        fbid: int
            | Specify the factor backtest id.

        data: bool, default True
            | Include dataframe in returned value.

        report: bool, default False
            | Open interactive GUI report in web browser at the end of the process.

            .. admonition:: Warning
                :class: warning

                Either data or report should be True.

    Returns
    -------
        report = True
            Open interactive Factor Backtest Report.

        data = True
            | data : dictionary of dataframes

            - *summary: summary of factorbacktest job*
            - *ar: annual return*
            - *counts: number of securities in each bin*
            - *ic: information coefficient*
            - *pnl: profit & losses*
            - *qr: quantile return*
            - *to: turnover*


    Examples
    --------
        >>> prism.factor_backtest_jobs()
        jobid            jobname  jobstatus  ...  factorbacktestid  avg_turnover    avg_ic  top_bottom_spread  frequency  bins  max_days  rank_method  description                   period
        0      1  factor_backtest_1  Completed  ...                 1      0.475282  0.017800          -0.000383          Q  10.0      93.0     standard         None  2013-01-01 ~ 2015-01-01

        >>> prism.get_factor_backtest_result(1, report=True)
        Fetching A Link to Factor Backtest Report...
        Link to Factor Backtest Report:
        https://ext.prism39.com/report/factor_backtest/my_username_1_14798b70-4a7a-4606-8179-44f6932f34e6/
        Fetching Factor Backtest Result Data...
        {
            'ar':
                Top-Bottom Spread     Bin 1     Bin 2     Bin 3     Bin 4     Bin 5     Bin 6     Bin 7    Bin 8     Bin 9    Bin 10
                0          -0.000383  0.002693  0.001911  0.001745  0.001602  0.001693  0.001987  0.001952  0.00193  0.002166  0.002148,
            'counts':
                            date  Bin 1  Bin 2  Bin 3  Bin 4  Bin 5  Bin 6  Bin 7  Bin 8  Bin 9  Bin 10
                    0  2013-03-31     49     50     50     50     50     49     50     50     50      50
                    1  2013-06-30     49     49     50     49     50     49     49     50     49      50
                    2  2013-09-30     49     50     50     49     50     50     49     50     50      50
                    3  2013-12-31     49     49     49     49     49     49     49     49     49      50
                    4  2014-03-31     49     50     50     50     50     50     50     50     50      50
                    5  2014-06-30     50     50     50     50     50     50     50     50     50      50
                    6  2014-09-30     49     50     50     50     50     49     50     50     50      50
                    7  2014-12-31     49     50     50     50     50     49     50     50     50      50,
            'ic':        date         ic
                0  2013-03-31   0.109810
                1  2013-06-30  -0.024280
                2  2013-09-30   0.073506
                3  2013-12-31  -0.007544
                4  2014-03-31  -0.034033
                5  2014-06-30  -0.035701
                6  2014-09-30   0.042841,
            'pnl':       date  Top-Bottom Spread     Bin 1     Bin 2     Bin 3     Bin 4     Bin 5     Bin 6     Bin 7     Bin 8     Bin 9    Bin 10
                0  2013-03-31          -0.026218  0.107641  0.025149  0.020147  0.029949  0.025136  0.030979  0.047745  0.050728  0.053055  0.081424
                1  2013-06-30          -0.040646  0.198980  0.095820  0.069968  0.070595  0.093182  0.100881  0.102511  0.113004  0.111119  0.154577
                2  2013-09-30          -0.017259  0.327730  0.210149  0.150424  0.158664  0.203366  0.209441  0.189935  0.221166  0.229827  0.306704
                3  2013-12-31          -0.041429  0.406996  0.233885  0.190352  0.175839  0.225944  0.246494  0.231905  0.218980  0.286169  0.352579
                4  2014-03-31          -0.077449  0.530770  0.313009  0.254870  0.254214  0.268607  0.292174  0.316257  0.289976  0.334870  0.420739
                5  2014-06-30          -0.097823  0.533991  0.319311  0.267409  0.233913  0.252408  0.294491  0.305149  0.266159  0.332309  0.392353
                6  2014-09-30          -0.076550  0.539356  0.382519  0.349352  0.320580  0.338911  0.397894  0.390694  0.386452  0.433719  0.430054,
            'qr':        date  Top-Bottom Spread     Bin 1     Bin 2     Bin 3      Bin 4      Bin 5     Bin 6      Bin 7      Bin 8      Bin 9     Bin 10
                0  2013-03-31          -0.026218  0.107641  0.025149  0.020147   0.029949   0.025136  0.030979   0.047745   0.050728   0.053055   0.081424
                1  2013-06-30          -0.014817  0.082462  0.068937  0.048838   0.039464   0.066378  0.067802   0.052270   0.059269   0.055138   0.067646
                2  2013-09-30           0.024377  0.107383  0.104332  0.075195   0.082261   0.100792  0.098611   0.079295   0.097180   0.106836   0.131760
                3  2013-12-31          -0.024594  0.059701  0.019615  0.034707   0.014824   0.018762  0.030637   0.035272  -0.001790   0.045813   0.035107
                4  2014-03-31          -0.037578  0.087971  0.064125  0.054201   0.066654   0.034799  0.036646   0.068472   0.058242   0.037865   0.050393
                5  2014-06-30          -0.022083  0.002104  0.004800  0.009992  -0.016187  -0.012769  0.001793  -0.008439  -0.018463  -0.001919  -0.019980
                6  2014-09-30           0.023579  0.003497  0.047910  0.064654   0.070238   0.069069  0.079880   0.065544   0.095006   0.076116   0.027077,
            'summary':    username  universename   startdate     enddate frequency  bins  avg_turnover  avg_ic  top_bottom_spread
                    0  my_username       S&P 500  2013-01-01  2015-01-01         Q    10      0.475282  0.0178          -0.000383,
            'to':       date  turnover
                0 2013-03-31  0.437751
                1 2013-06-30  0.459514
                2 2013-09-30  0.476861
                3 2013-12-31  0.549898
                4 2014-03-31  0.428858
                5 2014-06-30  0.452000
                6 2014-09-30  0.522088
        }
    """
    if isinstance(fbid, int):
        fbid = [fbid]
    return _get_task_result("factor_backtest", "Factor Backtest", fbid, data, report)


def get_strategy_backtest_result(fbid: int, data=True, report=False):
    return _get_task_result("strategy_backtest", "Strategy Backtest", [fbid], data, report)


@_validate_args
def _get_task_result(tasktype, tasktyperepr, resultid: list, data: bool = True, report: bool = True):
    if (data == False) and (report == False):
        raise PrismValueError("Either data or report should be true.")
    if report:
        # Format Definition:
        # Webclient Address/report/report_type/file_id?token=web_auth_token
        url_get_results = [URL_TASK + "/" + tasktype + "/report/" + str(i) for i in resultid]
        fileids = [get(url)["path"].values[0] for url in url_get_results]

        web_auth_token = _get_web_authentication_token()

        print("Fetching link to " + tasktyperepr + " Report...")
        for idx, i in enumerate(fileids):
            link = ROOT_EXT_WEB_URL + "/report/" + tasktype + "/" + str(i)
            print(f"Link to {tasktyperepr} Report {resultid[idx]}:")
            print(link)

        if len(resultid) == 1:
            link = link[:-1] + "?token=" + web_auth_token
            webbrowser.open(link, new=2)

    if data:
        url_get_results = [URL_TASK + "/" + tasktype + "/result/" + str(i) for i in resultid]
        print("Fetching " + tasktyperepr + " Result Data...")
        headers = _authentication()
        ret = {}
        for idx, i in enumerate(resultid):
            res = requests.get(url_get_results[idx], headers=headers)
            ret_dict = _process_fileresponse(res, "task_result", res.content, keep_dict=True)
            ret[i] = {k.split(".parquet")[0]: v for k, v in ret_dict.items()}
        return list(ret.values())[0] if len(ret) == 1 else ret
