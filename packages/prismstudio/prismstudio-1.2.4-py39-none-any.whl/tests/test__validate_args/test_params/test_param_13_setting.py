import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def get_setting(setting: str):
    return True


def test_setting_param(mocker):
    mocker.patch("prism._common.const.PreferenceType", ["mode", "size", "author"])

    # valid setting keys
    assert get_setting("mode")
    assert get_setting("size")
    assert get_setting("author")


def test_wrong_setting_param(mocker):
    mocker.patch("prism._common.const.PreferenceType", ["mode"])

    # wrong value
    with pytest.raises(PrismValueError):
        assert get_setting("unknown")

    with pytest.raises(PrismValueError):
        assert get_setting("my_mode")

    with pytest.raises(PrismValueError):
        assert get_setting("MODE")

    # wrong type
    with pytest.raises(PrismTypeError):
        assert get_setting(1)
