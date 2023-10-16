from typing import Union

import pytest

from prism._common.const import FrequencyType, UniverseFrequencyType
from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def get_universe(universe,
                 frequency: str = None,
                 shownid: list = None) -> UniverseFrequencyType:
    """
    valid frequency =
        'D', 'W', 'MS', 'SMS', 'SM', 'M', 'Q', 'QS', 'AS', 'A'
    """
    return frequency


def test_get_universe_frequency_param(mocker):
    mocker.patch("prism._common.const.SMValues", {
                 "apple": "prism_code1", "AAPL": "prism_code1", "prism39": "prism_code3"})

    assert get_universe("universe", frequency=None) is None

    # valid frequecy param
    assert get_universe("universe", frequency="D",
                        shownid=["AAPL"]) == UniverseFrequencyType.CALENDAR_DAY
    assert get_universe(
        "universe", frequency="W") == UniverseFrequencyType.WEEKS
    assert get_universe(
        "universe", frequency="MS") == UniverseFrequencyType.MONTH_START
    assert get_universe(
        "universe", frequency="SMS") == UniverseFrequencyType.SEMI_MONTH_START
    assert get_universe(
        "universe", frequency="SM") == UniverseFrequencyType.SEMI_MONTH_END
    assert get_universe(
        "universe", frequency="M") == UniverseFrequencyType.MONTH_END
    assert get_universe(
        "universe", frequency="Q") == UniverseFrequencyType.QUARTER_END
    assert get_universe(
        "universe", frequency="QS") == UniverseFrequencyType.QUARTER_START
    assert get_universe(
        "universe", frequency="AS") == UniverseFrequencyType.YEAR_START
    assert get_universe(
        "universe", frequency="A") == UniverseFrequencyType.YEAR_END


def test_get_universe_wrong_param(mocker):
    mocker.patch("prism._common.const.SMValues", {
                 "apple": "prism_code1", "AAPL": "prism_code1", "prism39": "prism_code3"})

    # wrong value
    with pytest.raises(Exception):
        assert get_universe(
            "universe", frequency="a") == UniverseFrequencyType.YEAR_END

    with pytest.raises(Exception):
        assert get_universe(
            "S&P 500", frequency="ms") == UniverseFrequencyType.MONTH_START

    with pytest.raises(Exception):
        assert get_universe("S&P 500", shownid=[
                            "AAPL"], frequency="random") is None

    # wrong type
    with pytest.raises(Exception):
        assert get_universe("S&P 500", frequency=222)

    with pytest.raises(Exception):
        assert get_universe("S&P 500", shownid=123)


@_validate_args
def factor_backtest(self,
                    jobname: Union[str, list] = None,
                    report: bool = True,
                    frequency: str = None) -> FrequencyType:
    """
    valid frequency =
        'N', 'U', 'us', 'L', 'ms', 'S', 'T', 'min', 'H', 'BH', 'D', 'BD', 'W', 'MS', 'BMS', 'SMS', 'SM', 'BM', 'M', 'Q', 'QS', 'BQ', 'BQS', 'AS', 'A'
    """
    return frequency


def test_frequency_param():
    assert factor_backtest("job1", frequency=None) is None

    # check type
    # assert isinstance(factor_backtest("job", frequency="N"), FrequencyType)

    # valid frequecy param
    assert factor_backtest("job", frequency="N") == FrequencyType.NANOSECONDS
    assert factor_backtest("job", frequency="U") == FrequencyType.MICROSECONDS
    assert factor_backtest(
        "job", frequency="us") == FrequencyType.MICROSECONDS_ALIAS
    assert factor_backtest("job", frequency="L") == FrequencyType.MILISECONDS
    assert factor_backtest(
        "job", frequency="ms") == FrequencyType.MILISECONDS_ALIAS
    assert factor_backtest("job", frequency="S") == FrequencyType.SECONDS
    assert factor_backtest("job", frequency="T") == FrequencyType.MINUTES
    assert factor_backtest(
        "job", frequency="min") == FrequencyType.MINUTES_ALIAS
    assert factor_backtest("job", frequency="H") == FrequencyType.HOURS
    assert factor_backtest(
        "job", frequency="BH") == FrequencyType.BUSINESS_HOURS
    assert factor_backtest("job", frequency="D") == FrequencyType.CALENDAR_DAY
    assert factor_backtest("job", frequency="BD") == FrequencyType.BUSINESS_DAY
    assert factor_backtest("job", frequency="W") == FrequencyType.WEEKS
    assert factor_backtest("job", frequency="MS") == FrequencyType.MONTH_START
    assert factor_backtest(
        "job", frequency="BMS") == FrequencyType.BUSINESS_MONTH_START
    assert factor_backtest(
        "job", frequency="SMS") == FrequencyType.SEMI_MONTH_START
    assert factor_backtest(
        "job", frequency="SM") == FrequencyType.SEMI_MONTH_END
    assert factor_backtest(
        "job", frequency="BM") == FrequencyType.BUSINESS_MONTH_END
    assert factor_backtest("job", frequency="M") == FrequencyType.MONTH_END
    assert factor_backtest("job", frequency="Q") == FrequencyType.QUARTER_END
    assert factor_backtest(
        "job", frequency="QS") == FrequencyType.QUARTER_START
    assert factor_backtest(
        "job", frequency="BQ") == FrequencyType.BUSINESS_QUARTER_END
    assert factor_backtest(
        "job", frequency="BQS") == FrequencyType.BUSINESS_QUARTER_START
    assert factor_backtest("job", frequency="AS") == FrequencyType.YEAR_START
    assert factor_backtest("job", frequency="A") == FrequencyType.YEAR_END


def test_wrong_frequency_param():
    # wrong value
    # with pytest.raises(Exception):
    #     assert factor_backtest("job", frequency="random_frequency")

    with pytest.raises(Exception):
        assert factor_backtest("job", frequency="a") == FrequencyType.YEAR_END

    # wrong type
    with pytest.raises(Exception):
        assert factor_backtest("job", frequency=123)

    with pytest.raises(Exception):
        assert factor_backtest("job", report=333)
