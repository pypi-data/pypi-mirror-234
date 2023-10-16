from typing import Union

import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError


@_validate_args
def add(r: int, l: int):
    return r + l


def test_add():
    assert add(1, 2) == 3
    assert add(1, 5) != 3

    with pytest.raises(PrismTypeError):
        assert add(1, '2') == 3

    with pytest.raises(PrismTypeError):
        assert add(1, 'five') == 6


def test_missing_argument_in_add():
    with pytest.raises((TypeError, PrismTypeError)):
        assert add(1)

    with pytest.raises((TypeError, PrismTypeError)):
        assert add(r=1)

    with pytest.raises((TypeError, PrismTypeError)):
        assert add()

    with pytest.raises((TypeError, PrismTypeError)):
        assert add(1, None)


@_validate_args
def same(r: int, l: float):
    return r, l


def test_same():
    assert same(1, 2.1) == (1, 2.1)
    assert same(1, 5.1) != 3

    # this is intended behavior
    assert same(1, None)
    # assert same(1) # will raise type error


def test_missing_argument_in_same():
    # explicit None can be ignored
    assert same(None, None) == (None, None)
    assert same(1, None) == (1, None)
    assert same(None, 2.0) == (None, 2.0)

    with pytest.raises((TypeError, PrismTypeError)):
        assert same(1)

    with pytest.raises((TypeError, PrismTypeError)):
        assert same(r=1)

    with pytest.raises((TypeError, PrismTypeError)):
        assert same()


@_validate_args
def concat(r: str = '', l: str = ''):
    return r + l


def test_concate():
    assert not concat()
    assert concat('a') == 'a'
    assert concat('a', 'b') == 'ab'
    assert concat(str(1), '2') == '12'

    with pytest.raises(PrismTypeError):
        assert concat('1', 2) == '12'

    with pytest.raises(PrismTypeError):
        assert concat(1, 'five') == '1five'


@_validate_args
def my_union(unionValue: Union[str, float, int]):
    return unionValue


def test_union():
    assert my_union(1) == 1
    assert my_union('abc') == 'abc'
    assert my_union(1.12) == 1.12

    with pytest.raises(PrismTypeError):
        assert not my_union({})

    with pytest.raises(PrismTypeError):
        assert my_union(lambda x: x)
