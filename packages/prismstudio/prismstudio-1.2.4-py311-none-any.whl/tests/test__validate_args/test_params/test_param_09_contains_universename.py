from typing import Union

import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def filter_universe(condition: list, universename: Union[str, list]):
    return True


condition = [{"attribute": 'CIQ primary',
              'value': ['primary'], 'operator': 'AND'}]


def test_universename_param():
    # valid universename
    assert filter_universe(condition, 'APAC_primary')
    assert filter_universe(condition, ['APAC_primary'])
    assert filter_universe(condition, [
                           'APAC_primary"', 'Hello! World!\n', 'THERE # is ? special @ char !! inside.'])
    assert filter_universe(condition, "This is OK`\"'To be inside")
    assert filter_universe(condition, "This is OK#\"'To be inside")
    assert filter_universe(condition, "This is OK#`'To be inside")


def test_wrong_universename_param():
    # wrong value (regex test)
    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "@`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "_`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "!`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "#`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "$`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "%`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "^`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "&`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "*`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "(`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, ")`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "<`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, ">`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "?`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "|`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "{`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "}`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "~`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, ":`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "APAC_!`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, "HELLO#`\"'")

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, ['APAC_primary', "SPECIAL#`\"'"])

    with pytest.raises(PrismValueError):
        assert filter_universe(condition, ["INSIDE@@@`\"'AA", 'APAC_primary'])

    # wrong type
    with pytest.raises(PrismTypeError):
        assert filter_universe(condition=condition, universename=1)

    with pytest.raises(PrismTypeError):
        assert filter_universe(condition=1)

    with pytest.raises((TypeError, PrismTypeError)):
        assert filter_universe(condition=condition)


def test_function_param_contains_univername():
    @_validate_args
    def sample_function(param_universename: str | list):
        return True

    assert sample_function("my universe")

    with pytest.raises(PrismValueError):
        assert sample_function("APAC#`\"'_primary")

    with pytest.raises(PrismValueError):
        assert sample_function(["@@@`\"'with special"])
