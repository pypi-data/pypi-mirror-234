import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismAuthError, PrismTypeError, PrismValueError


@_validate_args
def get_portfolio(
    universe: str,
    shownid: list
):
    return shownid


def test_shownid_param(mocker):
    mocker.patch("prism._common.const.SMValues", {
                 "apple": "prism_code1", "AAPL": "prism_code1", "prism39": "prism_code3"})

    # check type
    assert isinstance(get_portfolio('S&P 500', shownid=["prism39"]), list)

    assert get_portfolio('S&P 500', shownid=["prism39"]) == ["prism_code3"]
    assert get_portfolio('S&P 500', shownid=["PRISM39"]) == ["prism_code3"]
    assert get_portfolio('S&P 500', shownid=["AAPL", "Prism39"]) == [
        "prism_code1", "prism_code3"]
    assert get_portfolio('S&P 500', shownid=["    aapl", "prism_39"]) == [
        "prism_code1", "prism_code3"]
    assert get_portfolio('S&P 500', shownid=["a p p l e", "prism 39"]) == [
        "prism_code1", "prism_code3"]


def test_wrong_shownid_param(mocker):
    mocker.patch("prism._common.const.SMValues", {
                 "apple": "prism_code1", "AAPL": "prism_code1", "prism39": "prism_code3"})

    # wrong value
    with pytest.raises(PrismValueError):
        assert get_portfolio('S&P 500', ["aaapple"]) == ["prism_code1"]

    with pytest.raises(PrismValueError):
        assert get_portfolio('S&P 500', ["APPL"]) == ["prism_code1"]

    with pytest.raises(PrismValueError):
        assert get_portfolio('S&P 500', ["apple", "prism39", "unknown"]) == [
            "prism_code1", "prism_code1"]

    # wrong type
    with pytest.raises(PrismTypeError):
        assert get_portfolio('S&P 500', shownid=0)

    with pytest.raises(PrismTypeError):
        assert get_portfolio('S&P 500', shownid={"Apple": "AAPL"}) == [
            "prism_code1"]

    # wrong attribute
    with pytest.raises(AttributeError):
        assert get_portfolio('S&P 500', [123])

    with pytest.raises(AttributeError):
        assert get_portfolio('S&P 500', shownid=["Apple", 1234])


def test_auth_error_when_using_shownid_param(mocker):
    mocker.patch("prism._common.const.SMValues", None)

    # PrismAuthError
    with pytest.raises(PrismAuthError):
        assert get_portfolio('S&P 500', ["prism39"]) == ["prism_code3"]
