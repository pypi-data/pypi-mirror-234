import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError


@_validate_args
def log(base: int):
    return True


def test_base_param_in_function_log():
    assert log(1)

    # valid base param
    assert log(2)
    assert log(base=4)


def test_wrong_base_param_in_function_log():
    # wrong value
    with pytest.raises(Exception):
        assert log(0)

    with pytest.raises(Exception):
        assert log(-1)

    # wrong type
    with pytest.raises(PrismTypeError):
        assert log("1")

    with pytest.raises(PrismTypeError):
        assert log("info")


@_validate_args
def sample_function(base: int):
    return True


def test_base_param_in_sample_function():
    # all integers are valid
    assert sample_function(0)
    assert sample_function(-2)
    assert sample_function(2)
    assert sample_function(base=4)


def test_wrong_base_param_in_sample_function():
    # wrong type
    with pytest.raises(PrismTypeError):
        assert sample_function("1")

    with pytest.raises(PrismTypeError):
        assert sample_function("info")
