import copy
from typing import Union

import pandas as pd
import pyarrow as pa
import requests

from .._common.config import URL_TASK, URL_UNIVERSES, URL_UPLOAD
from .._common.const import TaskComponentType
from .._core._req_builder._universe import should_overwrite_universe
from .._core._req_builder._portfolio import should_overwrite_portfolio
from .._core._req_builder._exportdata import should_overwrite_datafile
from .._core._req_builder import _task
from .._prismcomponent.prismcomponent import _PrismTaskComponent
from .._core._req_builder._universe import should_overwrite_universe
from .._utils import _authentication, _validate_args, Loader, post, get, are_periods_exclusive
from .._utils.exceptions import PrismTaskError, PrismValueError, PrismTypeError


class _Screen(_PrismTaskComponent):
    _component_name = TaskComponentType.SCREEN

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    def run(
        self,
        newuniversename: str,
        jobname: str = None,
        frequency: str = None,
        startdate: str = None,
        enddate: str = None,
    ):
        """
        Enables users to quickly construct custom time-variant universes through user defined rules to evaluate over the specified startdate and endddate.

        Parameters
        ----------
            newuniversename : str
                Name of the universe to be created.

            jobname : str
                | Name of the job when the task component is run.
                | If None, the default job name sets to screen_{jobid}.

            frequency : str {'D', 'BD', 'W', 'BM', 'M', 'Q', 'A'}
                | Desired rebalancing frequency to run screen.
                | If specified, this will overwrite frequency parameter in the task component.

            startdate : str, default None
                | Startdate of the time period for which to load data or the window in time in which to run a task.
                | If specified, this will overwrite startdate parameter in the task component.

            enddate : str, default None
                | Enddate of the time period for which to load data or the window in time in which to run a task.
                | If specified, this will overwrite enddate parameter in the task component.

        Returns
        -------
            status : dict
                | Returns 'Pending' status.
                | Screening task is added to system task queue.

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
                    universename="S&P 500",
                    startdate="2010-01-01",
                    enddate="2015-01-01",
                    frequency="D",
                    )
            >>> snp_200_screen.run(newuniversename="snp_200")
            {'status': 'Pending',
            'message': 'screen pending',
            'result': [{'resulttype': 'jobid', 'resultvalue': 5}]}

            >>> prism.job_manager()
            >>> # Wait for the job 5 in GUI until its status changed to 'Completed'

            >>> prism.list_universe()
            universeid                 universename  universetype   startdate     enddate
            0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
            1           2                      S&P 500         index  1700-01-01  2199-12-31
            2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
            3           4           Russell 3000 Index         index  1700-01-01  2199-12-31
            4           5                      snp_200         index  2010-01-01  2015-01-01
        """
        should_overwrite, err_msg = should_overwrite_universe(newuniversename, "screening")
        if not should_overwrite:
            print(f"{err_msg}")
            return
        component_args = copy.deepcopy(self._query["component_args"])
        universeid = component_args.pop("universeid")
        component_args.update({"universeid": int(universeid)})

        universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
        universe_startdate = universe_info["Start Date"].values[0]
        universe_enddate = universe_info["End Date"].values[0]
        component_args.update({"newuniversepath": newuniversename + ".puv"})

        if frequency is not None:
            component_args["frequency"] = frequency
        if startdate is not None:
            component_args["startdate"] = startdate
        if enddate is not None:
            component_args["enddate"] = enddate

        universe_period_violated = are_periods_exclusive(
            universe_startdate, universe_enddate, component_args.get("startdate"), component_args.get("enddate")
        )

        if universe_period_violated:
            raise PrismValueError(
                f'Screen period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
            )

        query = {
            "component_type": self._component_type,
            "component_name": self._component_name,
            "component_args": component_args,
        }

        rescontent = None
        with Loader("Screen Running... ") as l:
            try:
                rescontent = post(URL_TASK + "/screen", params={"jobname": jobname}, body=query)
            except:
                l.stop()
                raise PrismTaskError("Screen has failed.")
            if rescontent["status"] != "Pending":
                l.stop()
                raise PrismTaskError("Screen has failed.")

        print(f'{rescontent["message"]}')
        return rescontent

class _ExportData(_PrismTaskComponent):
    _component_name = TaskComponentType.EXPORT_DATA

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    def run(
        self,
        exportdatapath: str,
        commponent_names: list = None,
        jobname: str = None,
        startdate: str = None,
        enddate: str = None,
    ):
        """
        Enables users to quickly retrieve and save specified components of data.

        Parameters
        ----------
            exportdatapath: str
                | File path of the exported data.

            component_names: list
                | List of component names in Export Data Task Component
                | Names have to be the same order as data component list in Task Component.

            jobname : str
                | Name of the job when the task component is run.
                | If None, the default job name sets to screen_{jobid}.

            startdate : str, default None
                | Startdate of the time period for which to load data or the window in time in which to run a task.
                | If specified, this will overwrite startdate parameter in the task component.

            enddate : str, default None
                | Enddate of the time period for which to load data or the window in time in which to run a task.
                | If specified, this will overwrite enddate parameter in the task component.

        Returns
        -------
            status : dict
                | Returns 'Pending' status.
                | Screening task is added to system task queue.

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
        should_overwrite, err_msg = should_overwrite_datafile(exportdatapath, "creating")
        if not should_overwrite:
            print(f"{err_msg}")
            return

        component_args = copy.deepcopy(self._query["component_args"])
        universeid = component_args.pop("universeid")
        component_args.update({"universeid": int(universeid)})



        if any([not isinstance(n, str) for n in commponent_names]):
            raise PrismTypeError('Name for each component shoud be string')
        if len(commponent_names) != len(component_args["dataqueries"]):
            raise PrismValueError(
                f'Number of names must be equal to the number of components'
            )

        universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
        universe_startdate = universe_info["Start Date"].values[0]
        universe_enddate = universe_info["End Date"].values[0]
        component_args.update({"exportdatapath": exportdatapath + ".ped"})
        component_args.update({"cmpts": commponent_names})

        if startdate is not None:
            component_args["startdate"] = startdate
        if enddate is not None:
            component_args["enddate"] = enddate

        universe_period_violated = are_periods_exclusive(
            universe_startdate, universe_enddate, component_args.get("startdate"), component_args.get("enddate")
        )

        if universe_period_violated:
            raise PrismValueError(
                f'Query period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
            )

        query = {
            "component_type": self._component_type,
            "component_name": self._component_name,
            "component_args": component_args,
        }

        rescontent = None
        with Loader("Export Data Running... ") as l:
            try:
                rescontent = post(URL_TASK + "/export_data", params={"jobname": jobname}, body=query)
            except:
                l.stop()
                raise PrismTaskError("Export Data has failed.")
            if rescontent["status"] != "Pending":
                l.stop()
                raise PrismTaskError("Export Data has failed.")

        print(f'{rescontent["message"]}')
        return rescontent

class _FactorBacktest(_PrismTaskComponent):
    _component_name = TaskComponentType.FACTOR_BACKTEST

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    def run(
        self,
        jobname: Union[str, list] = None,
        report: bool = True,
        frequency: str = None,
        bins: int = None,
        rank_method: str = None,
        max_days: int = None,
        startdate: str = None,
        enddate: str = None,
    ):
        """
        Enables users to quickly test and identify factors which may predict future return.

        Parameters
        ----------
            jobname : str
                | Name of the job when the task component is run.
                | If None, the default job name sets to factorbacktest_{jobid}.

            bins : int
                | Number of quantile portfolio the universe generate. Should be bigger than 1 and smaller than or equal to 20.
                | If specified, this will overwrite bins parameter in the task component.

                .. admonition: Note
                    :class: note

                    Bins are assigned to the factor score in descending order. Meaning the largest factor score will be assigned 1st bin

            startdate : str, default None
                | Startdate of the time period for which to load data or the window in time in which to run a task.
                | If specified, this will overwrite startdate parameter in the task component.

            enddate : str, default None
                | Enddate of the time period for which to load data or the window in time in which to run a task.
                | If specified, this will overwrite enddate parameter in the task component.

            max_days : int, default None
                | If None, default max days is induced from rebalancing frequency.
                | If specified, this will overwrite max_days parameter in the task component.

            rank_method : str {'standard', 'modified', 'dense', 'ordinal', 'fractional'}, default 'standard'
                | Method for how equal values are assigned a rank.

                - standard : 1 2 2 4
                - modified : 1 3 3 4
                - dense : 1 2 2 3
                - ordinal : 1 2 3 4
                - fractional : 1 2.5 2.5 4

                | Desired rebalancing frequency to run screen.
                | If specified, this will overwrite rank_method parameter in the task component.

        Returns
        -------
            status : dict
                Status of factorbacktest run.

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
            >>> fb_price_mom.run(jobname="factor_backtest_ep")
            factor_backtest is added to worker queue!: jobid is 1

            >>> prism.job_manager()
            >>> # Wait for the job 1 in GUI until its status changed to 'Completed'

            >>> prism.get_factor_backtest_result(1)
            Done!
            factor_backtest Completed: factorbacktestid is 1
            Fetching A Link to Factor Backtest Report...
            Link to Factor Backtest Report:
            https://ext.prism39.com/report/factor_backtest/my_username_1_afc7730c-55e6-41a8-ad4f-77df20caecc9/
        """
        component_args = copy.deepcopy(self._query["component_args"])
        universeid = component_args.pop("universeid")
        component_args["universeid"] = int(universeid)

        universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
        universe_startdate = universe_info["Start Date"].values[0]
        universe_enddate = universe_info["End Date"].values[0]

        if frequency is not None:
            component_args["frequency"] = frequency
        if bins is not None:
            component_args["bins"] = bins
        if rank_method is not None:
            component_args["rank_method"] = rank_method
        if max_days is not None:
            component_args["max_days"] = max_days
        if startdate is not None:
            component_args["startdate"] = startdate
        if enddate is not None:
            component_args["enddate"] = enddate

        universe_period_violated = are_periods_exclusive(
            universe_startdate, universe_enddate, component_args.get("startdate"), component_args.get("enddate")
        )

        if universe_period_violated:
            raise PrismValueError(
                f'Factor Backtest period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
            )

        if (component_args["bins"] < 2) or (component_args["bins"] > 20):
            PrismValueError("The number of bins should be between 2 and 20")
        for i in range(len(component_args["factor_dataquery"])):
            if isinstance(component_args["factor_dataquery"][i], pd.DataFrame):
                headers = {"Authorization": _authentication()["Authorization"], "Client-Channel": "python-extension"}
                batch = pa.record_batch(component_args["factor_dataquery"][i])
                sink = pa.BufferOutputStream()
                with pa.ipc.new_stream(sink, batch.schema) as writer:
                    writer.write_batch(batch)
                res = requests.post(URL_UPLOAD, files={"file": sink.getvalue()}, headers=headers)
                if res.ok:
                    path = res.json()["rescontent"]["data"]["url"]

                component_args["factor_dataquery"][i] = path
        query = {
            "component_type": self._component_type,
            "component_name": self._component_name,
            "component_args": component_args,
        }
        custom_data = [isinstance(f, str) for f in component_args["factor_dataquery"]]

        rescontent = None
        with Loader("Factor Backtest Running... ") as l:
            try:
                rescontent = post(
                    URL_TASK + "/factor_backtest",
                    params={"jobname": jobname, "custom_data": custom_data},
                    body=query,
                )
            except:
                l.stop()
                raise PrismTaskError("Factor Backtest has failed.")
            if rescontent["status"] != "Pending":
                l.stop()
                raise PrismTaskError("Factor Backtest has failed.")

        print(
            f'{rescontent["message"]}: {rescontent["result"][0]["resulttype"]} is {rescontent["result"][0]["resultvalue"]}'
        )
        # return _task._get_task_result(
        #     "factor_backtest",
        #     "Factor Backtest",
        #     [int(i["resultvalue"]) for i in rescontent["result"]],
        #     data=False,
        #     report=report,
        # )


class _StrategyBacktest(_PrismTaskComponent):
    _component_name = TaskComponentType.STRATEGY_BACKTEST

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    def run(self, portfolioname: str, jobname: str = None, report: bool = True):
        should_overwrite, err_msg = should_overwrite_portfolio(portfolioname, "constructing")
        if not should_overwrite:
            print(f"{err_msg}")
            return
        component_args = copy.deepcopy(self._query["component_args"])
        universeid = component_args.pop("universeid")
        benchmark = component_args.pop("benchmark")

        market_impact = {
            "model": component_args.pop("market_impact"),
            "model_value": component_args.pop("market_impact_value"),
        }
        commission_fee = {
            "model": component_args.pop("commission_fee"),
            "model_value": component_args.pop("commission_fee_value"),
        }
        short_loan_fee = {
            "model": component_args.pop("short_loan_fee"),
            "model_value": component_args.pop("short_loan_fee_value"),
        }
        risk_free_rate = {
            "model": component_args.pop("risk_free_rate"),
            "model_value": component_args.pop("risk_free_rate_value"),
        }
        margin_rate = {
            "model": component_args.pop("margin_rate"),
            "model_value": component_args.pop("margin_rate_value"),
        }
        cash_interest_rate = {
            "model": component_args.pop("cash_interest_rate"),
            "model_value": component_args.pop("cash_interest_rate_value"),
        }
        initial_position = {
            "position_type": component_args.pop("initial_position_type"),
            "position_value": component_args.pop("initial_position_value"),
        }

        task_params = {
            "portfoliopath": portfolioname + ".ppt",
            "universeid": universeid,
            "trade_value_type": "trade",
            "market_impact": market_impact,
            "commission_fee": commission_fee,
            "short_loan_fee": short_loan_fee,
            "risk_free_rate": risk_free_rate,
            "margin_rate": margin_rate,
            "cash_interest_rate": cash_interest_rate,
            "benchmark": benchmark,
            "initial_position": initial_position,
        }
        task_params.update(component_args)
        query = {
            "component_type": "taskcomponent",
            "component_name": "strategy_backtest",
            "component_args": task_params,
        }

        rescontent = None
        with Loader("Strategy Backtest Running... ") as l:
            try:
                rescontent = post(URL_TASK + "/strategy_backtest", params={"jobname": jobname}, body=query)
            except:
                l.stop()
                raise PrismTaskError("Strategy Backtest has failed.")
            if rescontent["status"] != "Pending":
                l.stop()
                raise PrismTaskError("Strategy Backtest has failed.")

        for r in rescontent["result"]:
            if r["resulttype"] == "strategybacktestid":
                sb_result = r["resultvalue"]
        print(
            f'{rescontent["message"]}: {rescontent["result"][0]["resulttype"]} is \
                {rescontent["result"][0]["resultvalue"]}, {rescontent["result"][1]["resulttype"]} is \
                    {rescontent["result"][1]["resultvalue"]}'
        )
        return _task._get_task_result("strategy_backtest", "Strategy Backtest", int(sb_result), report)
