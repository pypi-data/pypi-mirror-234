import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def get_settings(settings: dict):
    return True


def test_setting_param(mocker):
    mocker.patch("prism._common.const.PreferenceType", ["mode", "size", "author"])

    # valid setting keys
    assert get_settings({"mode": "white"})
    assert get_settings({"size": "10px"})
    assert get_settings({"author": "prism"})


def test_wrong_setting_param(mocker):
    mocker.patch("prism._common.const.PreferenceType", ["mode"])

    # wrong value
    with pytest.raises(PrismValueError):
        assert get_settings({"unknown": ""})

    with pytest.raises(PrismValueError):
        assert get_settings({"my_mode": ""})

    with pytest.raises(PrismValueError):
        assert get_settings({"MODE": ""})

    # wrong type
    with pytest.raises(PrismTypeError):
        assert get_settings(["mode"])
