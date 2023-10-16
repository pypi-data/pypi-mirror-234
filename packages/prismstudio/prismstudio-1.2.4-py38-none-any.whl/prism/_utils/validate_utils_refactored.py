import inspect
import re
from functools import wraps
from typing import Any, Callable

import pandas as pd

from prism._utils.exceptions import PrismTypeError, PrismValueError
from prism._utils.validate_utils import get_sm_attributevalue
from .._common.const import *


def _validate_args_refactored(function):
    signature = inspect.signature(function)

    @wraps(function)
    def type_checker(*args, **kwargs):
        try:
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            bound_args_dict = dict(bound_args.arguments)

            validate_fillna_function(bound_args_dict, function)

            for param_name, param_info in signature.parameters.items():
                if param_name == "self":
                    continue

                arg = bound_args_dict[param_name]
                if arg is None:
                    continue

                param_type = param_info.annotation

                check_argument_type(arg, param_type, param_name)

                arg = apply_validation_rules(
                    arg, param_name, function.__name__)

                bound_args_dict[param_name] = arg

            return function(**bound_args_dict)
        except TypeError as e:
            raise PrismTypeError(f"{e}")

    return type_checker


def validate_fillna_function(args_dict, function):
    if function.__name__ == "fillna":
        v, m = args_dict.get("value"), args_dict.get("method")
        if not (v is not None) ^ (m is not None):
            raise PrismValueError("Must specify one fill 'value' or 'method'.")


def check_argument_type(arg, param_type, param_name):
    if param_type is inspect.Parameter.empty:
        return

    if isinstance(param_type, type):
        if not isinstance(arg, param_type):
            raise PrismTypeError(
                f"Type of {param_name} is {type(arg)} and not {param_type}")
    elif not any(isinstance(arg, t) for t in param_type.__args__):
        raise PrismTypeError(
            f"Type of {param_name} is {type(arg)} and not in the Union of {param_type.__args__}")


def apply_validation_rules(arg, param_name: str, function_name: str):
    # if param_name equals function name
    if param_name in validation_functions:
        validation_function = validation_functions[param_name]
        return validation_function(arg, function_name)

    # if param_name matches custom pattern
    for _, (pattern_checker, validation_function) in custom_validation_functions.items():
        if pattern_checker(param_name):
            return validation_function(arg)

    # when there is no validation rule to check
    return arg


def frequency_param_validater(arg, function_name):
    if function_name == "get_universe":
        try:
            return UniverseFrequencyType(arg)
        except Exception as e:
            raise PrismValueError(
                f"{e}", valid_list=UniverseFrequencyType) from e
    else:
        try:
            return FrequencyType(arg)
        except Exception as e:
            raise PrismValueError(f"{e}", valid_list=FrequencyType) from e


def datetype_param_validater(arg, _):
    try:
        return DateType(arg)
    except Exception as e:
        raise PrismValueError(f"{e}", valid_list=DateType) from e


def periodtype_param_validater(arg, _):
    try:
        return PeriodType(arg)
    except Exception as e:
        raise PrismValueError(f"{e}", valid_list=PeriodType) from e


def adjustment_param_validater(arg, _):
    if arg not in [a.value for a in AdjustmentType]:
        # need review. original code 'e' is not bounded
        raise PrismValueError(
            'Invalid adjustment argument is given. ', valid_list=AdjustmentType)

    return arg


def shownid_param_validater(arg, _):
    for idx, id in enumerate(arg):
        arg[idx] = get_sm_attributevalue(id)

    return arg


def rank_method_param_validater(arg, _):
    try:
        return RankType(arg)
    except Exception as e:
        raise PrismValueError(f"{e}", valid_list=RankType) from e


def method_param_validater(arg, _):
    try:
        return FillnaMethodType(arg)
    except Exception as e:
        raise PrismValueError(f"{e}", valid_list=FillnaMethodType) from e


def startdate_param_validater(arg, _):
    try:
        date = pd.to_datetime(arg)
    except Exception as e:
        raise PrismValueError(
            f'Unknown string format. Cannot parse "{arg}" to a date') from e

    assert (date >= BEGINNING_DATE) & (
        date <= ACTIVE_DATE), "Not a valid date."

    return arg


def enddate_param_validater(arg, _):
    return startdate_param_validater(arg, _)


def base_param_validater(arg, function_name):
    if function_name == "log" and arg <= 0:
        raise Exception("base condition error")

    return arg


def preliminary_param_validater(arg, _):
    try:
        return FinancialPreliminaryType(arg)
    except Exception as e:
        raise PrismValueError(
            f"{e}", valid_list=FinancialPreliminaryType) from e


def setting_param_validater(arg, _):
    from .._common.const import PreferenceType
    if (arg not in PreferenceType) and (arg != ""):
        raise PrismValueError(
            "Invalid preference keyword is given. ", valid_list=PreferenceType)

    return arg


def settings_param_validater(arg, _):
    from .._common.const import PreferenceType
    for k in arg.keys():
        if k not in PreferenceType:
            raise PrismValueError(
                "Invalid preference key is given. ", valid_list=PreferenceType)

    return arg


# if param_name equals dict's key name
# TODO: refactor this code using eval
validation_functions: dict[str, Callable[[Any, str], Any]] = {
    "frequency": frequency_param_validater,
    "datetype": datetype_param_validater,
    "periodtype": periodtype_param_validater,
    "adjustment": adjustment_param_validater,
    "shownid": shownid_param_validater,
    "rank_method": rank_method_param_validater,
    "method": method_param_validater,
    "startdate": startdate_param_validater,
    "enddate": enddate_param_validater,
    "base": base_param_validater,
    "preliminary": preliminary_param_validater,
    "setting": setting_param_validater,
    "settings": settings_param_validater
}

# custom validaters


def custom_universename_validator(arg):
    regex = re.compile("[@_!#$%^&*()<>?/|}{~:]`\"'")
    if isinstance(arg, list):
        for a in arg:
            if regex.search(a) is not None:
                raise PrismValueError(
                    "universename not to include special characters")
    else:
        if regex.search(arg) is not None:
            raise PrismValueError(
                "universename not to include special characters")

    return arg


def custom_min_periods_validator(arg):
    if arg < 1:
        raise PrismValueError("min_periods cannot be less than 1")

    return arg


# uses custum pattern to check param_name
custom_validation_functions: dict[str, tuple[Callable[[str], bool], Callable[[Any], Any]]] = {
    "universename": (lambda param_name: "universename" in param_name, custom_universename_validator),
    "min_periods": (lambda param_name: "min_periods" in param_name, custom_min_periods_validator)
}
