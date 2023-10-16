import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def n_periods_intercept(x=None, y=None, n: int = 1, min_periods: int = 1):
    return True


def test_min_periods_param():
    assert n_periods_intercept(min_periods=1)

    # valid min_periods param
    assert n_periods_intercept(min_periods=1)
    assert n_periods_intercept(min_periods=2)
    assert n_periods_intercept(min_periods=9)
    assert n_periods_intercept(min_periods=9 // 3)
    assert n_periods_intercept(
        min_periods=9999999999999999999999999999999999999999999999999999999999999999999999999999999999)


def test_wrong_datetype_param():
    # wrong value
    with pytest.raises(PrismValueError):
        assert n_periods_intercept(min_periods=0)

    with pytest.raises(PrismValueError):
        assert n_periods_intercept(min_periods=-1)

    with pytest.raises(PrismValueError):
        assert n_periods_intercept(min_periods=20 * -1)

    # wrong type
    with pytest.raises(PrismTypeError):
        assert n_periods_intercept(min_periods=9 / 3)

    with pytest.raises(PrismTypeError):
        assert n_periods_intercept(min_periods="1")


def test_function_param_contains_min_periods():
    @_validate_args
    def sample_function(param_min_periods: int, min_periods_param: int = 1):
        return True

    assert sample_function(param_min_periods=1)
    assert sample_function(param_min_periods=2, min_periods_param=2)

    with pytest.raises(PrismValueError):
        assert sample_function(param_min_periods=-1)

    with pytest.raises(PrismValueError):
        assert sample_function(param_min_periods=1, min_periods_param=-1)
