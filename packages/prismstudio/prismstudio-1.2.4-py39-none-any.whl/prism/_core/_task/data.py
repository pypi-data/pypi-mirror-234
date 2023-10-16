import copy
from typing import Union
import warnings

from ..._common.config import *
from ..._common.config import URL_TASK, URL_UNIVERSES
from ..._common import const
from ..._core._req_builder._universe import parse_universe_to_universeid
from ..._core._req_builder._exportdata import should_overwrite_datafile
from ..._utils import (
    get as _get,
    _validate_args,
    are_periods_exclusive,
    get_sm_attributevalue,
    Loader, post as _post, are_periods_exclusive,
)
from ..._utils.exceptions import PrismTaskError, PrismValueError, PrismTypeError, PrismAuthError
from ..._prismcomponent import abstract_prismcomponent
from ..._prismcomponent.prismcomponent import _PrismTaskComponent


_data_category = __name__.split(".")[-1]


class PrismDataTaskComponent(_PrismTaskComponent):
    _component_category_repr = _data_category


class export_data(_PrismTaskComponent):
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
        ==== export_data
            Query Structure
        >>> ed.run("filepath/close", ["close", "open"])
        export_data is added to worker queue!
        {'status': 'Pending',
        'message': 'export_data is added to worker queue!',
        'result': [{'resulttype': 'jobid', 'resultvalue': 465}]}
    """
    @_validate_args
    def __init__(
        self,
        component: Union[abstract_prismcomponent._AbstractPrismComponent, list],
        universe: Union[str, int] = None,
        startdate: str = None,
        enddate: str = None,
        shownid: list = None,
        display_pit: bool = True,
        name: Union[str, list] = None,
    ):
        query = []
        cmpts = set()
        if isinstance(name, list) & (name is not None):
            if any([not isinstance(n, str) for n in name]):
                raise PrismTypeError('Names shoud be string')

        def add_cmpts(o):
            cmpts = set()
            if o["component_type"] == "datacomponent":
                cmpts.add(o["componentid"])
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

        if all((~const.DataComponents[const.DataComponents["componentid"].isin(cmpts)]["need_universe"]).tolist()):
            universeid = None
        else:
            universeid, _ = parse_universe_to_universeid(universe)

        universe_info = _get(f"{URL_UNIVERSES}/{universeid}/info")
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
        component_names = set([c._query["component_name"] for c in component])
        if const.FunctionComponents is None:
            raise PrismAuthError("Please Login First")
        aggregatecomponents = set(const.FunctionComponents[const.FunctionComponents["is_aggregate"]]["component_name_repr"].unique())
        if (len(component_names - aggregatecomponents) == 0) & (shownid is not None):
            warnings.warn(f"Shownid will be ignored for: {list(component_names & aggregatecomponents)}")

        super().__init__(
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
            ==== export_data
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

        universe_info = _get(f"{URL_UNIVERSES}/{universeid}/info")
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
            "component_type": self._query["component_type"],
            "component_name": self._query["component_name"],
            "component_args": component_args,
        }

        rescontent = None
        with Loader("Export Data Running... ") as l:
            try:
                rescontent = _post(URL_TASK + "/export_data", params={"jobname": jobname}, body=query)
            except:
                l.stop()
                raise PrismTaskError("Export Data has failed.")
            if rescontent["status"] != "Pending":
                l.stop()
                raise PrismTaskError("Export Data has failed.")

        print(f'{rescontent["message"]}')
        return rescontent

    @classmethod
    def list_job(cls):
        """
        List all export_data jobs.
        """
        return cls._list_job()