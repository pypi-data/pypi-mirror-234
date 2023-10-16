import copy
import requests
from typing import Union

from ..._common.config import *
from ..._common.const import UniverseFrequencyType as _UniverseFrequencyType
from ._list import _list_dataitem
from .preference import get_quiet_mode
from ..._utils import (
    _validate_args,
    get,
    post,
    patch,
    delete,
    get_sm_attributevalue,
    _authentication,
    _process_response,
    _process_fileresponse,
    _fetch_and_parse,
    plot_tree,
    are_periods_exclusive,
)
from ..._utils.exceptions import PrismNotFoundError, PrismValueError


__all__ = [
    "list_universe",
    "get_universe",
    "upload_universe",
    "save_index_as_universe",
    "combine_universe",
    "rename_universe",
    "delete_universe",
    "get_universe_template",
    "filter_universe",
]


@_validate_args
def list_universe(search: str = None, tree=False):
    """
    Return the all usable universes.

    Parameters
    ----------
        search : str, default None
            | Search word for universe name, the search is case-insensitive.
            | If None, the entire list is returned.

        tree : bool, default False
            | If True, the folder structure of the universes is visualized in a UNIX-style.

    Returns
    -------
        str or pandas.DataFrame
            | If tree is True, print file system tree of universes.
            | If tree is False, return usable universes in DataFrame.
            | Columns:

            - *universeid*
            - *universename*
            - *universetype*
            - *startdate*
            - *enddate*

    Examples
    --------
        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31
    """
    universes_df = _fetch_and_parse(URL_UNIVERSES, "puv", search)
    if universes_df.empty:
        raise PrismNotFoundError("No Universes found.")
    if not tree:
        return universes_df
    plot_tree(universes_df["universename"].tolist(), "universe")


@_validate_args
def get_universe(
    universe,
    startdate: str = None,
    enddate: str = None,
    frequency: str = None,
    shownid: list = None,
):
    """
    Return the specified universe in dataframe.

    Parameters
    ----------
        universe : str or int
            Universe name (str) or universe id (int) to get.

        startdate : str, default None
            | Start date of the data. The data includes start date.
            | If None, the start date of the universe is used. The same applies when the input is earlier than the universe start date.

        enddate : str, default None
            | End date of the data. The data excludes end date.
            | If None, the end date of the universe is used. The same applies when the input is later than the universe end date.

        frequency : str, {'D', 'W', 'MS', 'SMS', 'SM', 'M', 'Q', 'QS', 'AS', 'A'}
            | Desired sampling frequency of universe constituents. If expand is False, this parameter is ignored.

        shownid : list, default None
            | List of Security Master attributes to display with the data.
            | If None, default attributes set in preferences is shown.
            | If empty list ([]), no attribute is shown.

    Returns
    -------
        pandas.DataFrame
            Universe.
            Columns:
            - *listingid*
            - *date*
            - *attributes provided by the user via 'shownid'*

    Examples
    --------
        >>> prism.list_universe()
           universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31

        >>> prism.get_universe(univese='Russell 3000 Index')
                  listingid        date
        0           2585895  1978-12-29
        1           2586016  1978-12-29
        2           2586064  1978-12-29
        3           2586086  1978-12-29
        4           2586118  1978-12-29
        ...             ...         ...
        10110503  701835357  2199-12-31
        10110504  701932931  2199-12-31
        10110505  703822433  2199-12-31
        10110506  704721046  2199-12-31
        10110507  706171023  2199-12-31

        >>> prism.get_universe('Russell 3000 Index', startdate='2010-01-01', enddate='2015-12-31', shownid=['companyname'])
                listingid        date                   companyname
        0          2585893  2010-01-03                      AAON INC
        1          2585895  2010-01-03                      AAR CORP
        2          2585957  2010-01-03    ADC TELECOMMUNICATIONS INC
        3          2586016  2010-01-03            ABM INDUSTRIES INC
        4          2586068  2010-01-03            AEP INDUSTRIES INC
        ...            ...         ...                           ...
        2194810  325621650  2015-12-27        AVAGO TECHNOLOGIES LTD
        2194811  325832671  2015-12-27                     POZEN INC
        2194812  326004249  2015-12-27  LIBERTY INTERACTV CP QVC GRP
        2194813  344286611  2015-12-27            ITT INDUSTRIES INC
        2194814  365743684  2015-12-27     HERTZ GLOBAL HOLDINGS INC
    """

    universeid, _ = parse_universe_to_universeid(universe)

    universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
    universe_startdate = universe_info["Start Date"].values[0]
    universe_enddate = universe_info["End Date"].values[0]

    universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

    if universe_period_violated:
        raise PrismValueError(
            f'Universe query period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
        )

    if (frequency is not None) and (startdate is None):
        raise PrismValueError(f"Please provide startdate to resample with frequency {frequency}")

    default_shownid = True
    if (shownid is not None) and (len(shownid) == 0):
        shownid = None
        default_shownid = False
    if shownid is not None:
        shownid = [get_sm_attributevalue(a) for a in shownid]

    params = {
        "startdate": startdate,
        "enddate": enddate,
        "shownid": shownid,
        "default_shownid": default_shownid,
        "frequency": frequency,
    }
    headers = _authentication()
    res = requests.get(URL_UNIVERSES + f"/{universeid}", params=params, headers=headers)
    ret, _ = _process_fileresponse(res, res.content)
    return list(ret.values())[0]


@_validate_args
def upload_universe(universefile: str, universename: str):
    """
    Create a new universe with a csv file specifying the universe constituents. The csv file should have four columns: valuetype, value, startdate, enddate.
    “valuetype” specifies the Security Master attribute. “value” indicates the value of such attribute to include into the universe. “startdate” and “enddate” indicates the time range of specified security to be included into the universe.

    Parameters
    ----------
        universefile: str
            Path to the csv file to upload.
        universename: str
            Name of the universe to be created.

    Returns
    -------
        status: dict
            Status of upload_universe.

    Examples
    --------
        >>> import pandas as pd
        >>> universe_df = pd.read_csv("./my_universe.csv")
        >>> universe_df # include all securities being traded in the Korean Exchange
        valuetype  value   startdate     enddate
        0        MIC   XKRX  1700-01-01  2999-12-31

        >>> prism.upload_universe(universefile="./my_universe.csv", universename="krx")
        {'status': 'Success',
        'message': 'Universe saved',
        'result': [{'resulttype': 'universeid', 'resultvalue': 1}]}

        >>> prism.list_universe()
        universeid  universename  universetype   startdate     enddate
        0           1           krx        custom  1700-01-01  2199-12-31

    """
    should_overwrite, err_msg = should_overwrite_universe(universename, "uploading")
    if not should_overwrite:
        return err_msg
    universefile_params = {"universefile": open(universefile, "rb")}
    headers = {"Authorization": _authentication()["Authorization"], "client": "python"}
    res = requests.post(
        url=URL_UNIVERSES + "/flatfile",
        params={"path": universename + ".puv"},
        files=universefile_params,
        headers=headers,
    )
    ret = _process_response(res)
    print(f'{ret["message"]}: {ret["result"][0]["resulttype"]} is {ret["result"][0]["resultvalue"]}')
    return ret


@_validate_args
def save_index_as_universe(
    dataitemid: int,
    startdate: str = None,
    enddate: str = None,
    universename: str = None,
):
    """
    Create a new universe containing the constituents of an index.

    Parameters
    ----------
        dataitemid : int
            Unique identifier for the different data item. This identifies the index.
        startdate: str, default None
            Start date of the data. The data includes start date.
            If None, the start date of the universe is used. The same applies when the input is earlier than the universe start date.
        enddate: str, default None
            End date of the data. The data excludes end date.
            If None, the end date of the universe is used. The same applies when the input is later than the universe end date.
        universename: str, default None
            Name of the universe to be saved from the index.
            If None, the index name is used.


    Returns
    -------
        status: dict
            Status of save_index_as_universe.

    Examples
    --------
        >>> prism.index.universe_dataitems("S&P 500")
            dataitemid                                       dataitemname    datamodule       package
        0       4006682                                            S&P 500  S&P US Index  S&P US Index
        1       4006683           S&P 500 - Alternative Carriers (Sub Ind)	S&P US Index  S&P US Index
        2       4006684                 S&P 500 - Biotechnology (Industry)	S&P US Index  S&P US Index
        3       4006685                  S&P 500 - Biotechnology (Sub Ind)	S&P US Index  S&P US Index
        4       4006686                   S&P 500 - Broadcasting (Sub Ind)  S&P US Index  S&P US Index
        ...	        ...	                                               ...           ...           ...
        308     4006990                  S&P 500 Water Utilities (Sub Ind)	S&P US Index  S&P US Index
        309     4006991  S&P 500 Wireless Telecommunication Services (I...  S&P US Index  S&P US Index
        310     4006992  S&P 500 Wireless Telecommunication Services (S...  S&P US Index  S&P US Index
        311     4006993                      S&P 500 Oil (Composite) Index	S&P US Index  S&P US Index
        312     4006994  S&P 500 Semiconductors (Sub Ind)(30-APR-03) In...  S&P US Index  S&P US Index

        >>> prism.save_index_as_universe(dataitemid=4006682)
        {'status': 'Success',
        'message': 'Universe saved',
        'result': [{'resulttype': 'universeid', 'resultvalue': 1}]}

        >>> prism.list_universe()
        universeid  universename  universetype   startdate     enddate
        0           1       S&P 500         index  1700-01-01  2199-12-31
    """

    if universename is None:
        indices = _list_dataitem(
            datacategory = "Index",
            datacomponent = "Index Level",
        )
        universename = indices[indices["dataitemid"] == dataitemid]["dataitemname"].values[0]

    should_overwrite, err_msg = should_overwrite_universe(universename, "combining")
    if not should_overwrite:
        return err_msg
    params = {
        "dataitemid": dataitemid,
        "startdate": startdate,
        "enddate": enddate,
        "path": universename + ".puv",
    }
    ret = post(URL_UNIVERSES + f"/index", params, None)
    print(f'{ret["message"]}: {ret["result"][0]["resulttype"]} is {ret["result"][0]["resultvalue"]}')
    return ret


@_validate_args
def combine_universe(universes: list, newuniversename: str):
    """
    Create a new universe by combining existing universes.

    Parameters
    ----------
        universes: list of int or list of str
            List of universe id (int) or universe name (str) to combine.
        newuniversename: str
            Name of the universe to be created.

    Returns
    -------
        status: dict
            Status of combine universe.

    Examples
    --------
        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31

        >>> prism.combine_universe(["Korea Stock Price 200 Index", "S&P 500"], newuniversename="kospi_snp")
        {'status': 'Success',
        'message': 'Universe saved',
        'result': [{'resulttype': 'universeid', 'resultvalue': 1}]}

        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31
        4           5                    kospi_snp        custom  1700-01-01  2199-12-31

    """
    if len(universes) < 2:
        SystemExit("Please provide more than 2 universes to combine.")
    should_overwrite, err_msg = should_overwrite_universe(newuniversename, "saving")
    if not should_overwrite:
        return err_msg
    universeids = parse_universes_to_universeids(universes)
    params = {"universeids": universeids, "path": newuniversename + ".puv"}
    ret = post(URL_UNIVERSES + f"/combine", params, None)
    print(f'{ret["message"]}: {ret["result"][0]["resulttype"]} is {ret["result"][0]["resultvalue"]}')
    return ret


@_validate_args
def rename_universe(old: Union[str, int], new: str):
    """
    Rename universe. Location of universe within the folder structure can be changed using the method.

    Parameters
    ----------
        old: str or int
            Name of existing universe (str) or universe id (int) to be renamed.
        new: str
            New name of the universe.

    Returns
    -------
        status: dict
            Status of rename universe.

    Examples
    --------
        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31

        >>> prism.rename_universe(old='S&P 500', new='newname_snp')
        {'status': 'Success',
        'message': 'Universe renamed',
        'result': [{'resulttype': 'universeid', 'resultvalue': 2}]}

        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                  newname_snp         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31

    """
    should_overwrite, err_msg = should_overwrite_universe(new, "renaming")
    if not should_overwrite:
        return err_msg
    universeid, _ = parse_universe_to_universeid(old)
    ret = patch(URL_UNIVERSES + f"/{universeid}", {"newpath": new + ".puv"}, None)
    print(ret["message"])
    return ret


@_validate_args
def delete_universe(universe: Union[str, int]):
    """
    Delete universe.

    Parameters
    ----------
        universe : str or int
            Universe name (str) or universe id (int) to delete.

    Returns
    -------
        status: dict
            Status of delete_universe.

    Examples
    --------
        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           3    Russell 3000 Growth Index         index  1700-01-01  2199-12-31
        3           4           Russell 3000 Index         index  1700-01-01  2199-12-31

        >>> prism.delete_universe(universe='Russell 3000 Growth Index')
        {'status': 'Success',
        'message': 'Universe deleted',
        'result': [{'resulttype': 'universeid', 'resultvalue': 3}]}

        >>> prism.list_universe()
        universeid                 universename  universetype   startdate     enddate
        0           1  Korea Stock Price 200 Index         index  1700-01-01  2199-12-31
        1           2                      S&P 500         index  1700-01-01  2199-12-31
        2           4           Russell 3000 Index         index  1700-01-01  2199-12-31
    """
    universeid, _ = parse_universe_to_universeid(universe)
    ret = delete(URL_UNIVERSES + f"/{universeid}")
    print(ret["message"])
    return ret


def get_universe_template():
    """
    Get list of columns required for prism.upload_universe.

    Returns
    -------
        columns : list of str
            List of columns required for csv file to be uploaded.

    Examples
    --------
        >>> prism.get_universe_template()
        valuetype, value, startdate, enddate
    """
    res = requests.get(url=URL_UNIVERSES + "/template", headers=_authentication())
    return res.text


@_validate_args
def filter_universe(condition: list, universename: str):
    """
    Create a new universe from the entire Security Master using simple filter rules applied on Security Master attribute.

    Parameters
    ----------
        condition : list of dict
            List of security conditions to apply as filter. Each dictionary contains three keys: “operator”, “attribute”, “value”. Value must be a list

            - operator: {”AND”, “OR”}
            - attribute: Security Master attribute to condition on.
            - value: Value of Security Master attribute to condition on.
            - not: bool

        universename : str
            Name of the universe to be created.

    Returns
    -------
        status: dict
            Status of filter_universe.

    Examples
    --------
        >>> condition = [
            {'attribute': 'country', 'value': ['AU', 'NZ', 'HK', 'SG', 'JP', 'IN', 'ID', 'KR', 'MY', 'PH', 'TW', 'TH']},
            {'attribute': 'CIQ primary', 'value': ['primary'], 'operator': 'AND'}
            ]
        >>> prism.filter_universe(condition=condition, universename="APAC_primary")
        {'status': 'Success',
        'message': 'Universe saved',
        'result': [{'resulttype': 'universeid', 'resultvalue': 1}]}

        >>> prism.list_universe()
        universeid  universename  universetype   startdate     enddate
        0           1  APAC_primary         index  1700-01-01  2199-12-31
    """
    if len(condition) == 0:
        raise PrismValueError("At least one condition must be provided.")
    should_overwrite, err_msg = should_overwrite_universe(universename, "filtering")
    if not should_overwrite:
        return err_msg
    condition_copy = copy.deepcopy(condition)
    for i in range(len(condition)):
        assert isinstance(condition[i], dict), "condition must be list of dicts"
        assert set(condition[i].keys()) - {"operator", "isnot"} == {
            "attribute",
            "value"
        }, 'Valid arguments are "attribute", "value", "operator", and "isnot"'
        if not isinstance(condition[i]["value"], list):
            raise PrismValueError("Value must be a list")
        condition_copy[i]["attribute"] = get_sm_attributevalue(condition_copy[i]["attribute"])
        condition_copy[i]["isnot"] = condition[i].get("isnot", False)
    ret = post(URL_UNIVERSES + "/filter", {"path": universename + ".puv"}, condition_copy)
    print(f'{ret["message"]}: {ret["result"][0]["resulttype"]} is {ret["result"][0]["resultvalue"]}')
    return ret


@_validate_args
def parse_universe_to_universeid(universe: Union[str, int]):
    universes_df = _fetch_and_parse(URL_UNIVERSES, "puv")
    if universes_df.empty:
        raise PrismNotFoundError("No universe found.")

    if isinstance(universe, int):
        universes_df = universes_df[universes_df["universeid"] == universe]
    elif isinstance(universe, str):
        universes_df = universes_df[universes_df["universename"] == universe]
    else:
        raise PrismValueError("Please provide universe name or universe id for universe.")

    if universes_df.empty:
        raise PrismNotFoundError(f"No universe matching: {universe}", True, None)
    universeid = universes_df["universeid"].values[0]
    universename = universes_df["universename"].values[0]

    return universeid, universename


def parse_universes_to_universeids(universes: list):
    universes_df = _fetch_and_parse(URL_UNIVERSES, "puv")
    if universes_df.empty:
        raise PrismNotFoundError("No universe found.")

    universenames = []
    universeids = []
    for u in universes:
        if isinstance(u, int):
            universeids.append(u)
        elif isinstance(u, str):
            universenames.append(u)
        else:
            raise PrismValueError("Please provide universe name or universe id for universe.")

    ret_universeids = set()
    if len(universenames) != 0:
        matching_universes_df = universes_df[universes_df["universename"].isin(universenames)]
        if len(matching_universes_df) != len(universenames):
            not_matched = list(set(universenames) - set(matching_universes_df["universename"].tolist()))
            raise PrismNotFoundError(f"No universe matching: {not_matched}")
        universeids_from_universenames = matching_universes_df["universeid"].tolist()
        ret_universeids.update(universeids_from_universenames)

    if len(universeids) != 0:
        matching_universes_df = universes_df[universes_df["universeid"].isin(universeids)]
        if len(matching_universes_df) != len(universeids):
            not_matched = list(set(universeids) - set(matching_universes_df["universeid"].tolist()))
            raise PrismNotFoundError(f"No universe matching: {not_matched}")
        existing_universeids = matching_universes_df["universeid"].tolist()
        ret_universeids.update(existing_universeids)
    return list(ret_universeids)


def should_overwrite_universe(universename, operation):
    if get_quiet_mode():
        return True, None
    universes_df = _fetch_and_parse(URL_UNIVERSES, "puv")
    if universes_df.empty:
        return True, None

    if universename in universes_df["universename"].to_list():
        overwrite = input(f"{universename} already exists. Do you want to overwrite? (Y/N) \n")
        if overwrite.lower() == "y":
            return True, None
        elif overwrite.lower() == "n":
            return False, f"Not {operation} universe."
        else:
            return False, "Please provide a valid input."
    else:
        return True, None
