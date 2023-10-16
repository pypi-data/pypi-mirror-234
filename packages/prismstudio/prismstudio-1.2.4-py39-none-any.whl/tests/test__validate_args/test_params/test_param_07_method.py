import pytest

from prism._common.const import FillnaMethodType
from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def fillna(
        method: str,
        n: int = 0,
        value=None) -> FillnaMethodType:
    """
    valid arguments:
        'backfill', 'bfill', 'pad', 'ffill'
    """
    return method


def test_fillna_param():
    assert fillna(None, value=1, n=1) is None

    # check type
    # assert isinstance(fillna('backfill', n=1), FillnaMethodType)

    # # valid fillna param
    # assert fillna('backfill', n=1) == FillnaMethodType.BACKFILL
    # assert fillna('bfill', n=2) == FillnaMethodType.BFILL
    # assert fillna('pad', n=3) == FillnaMethodType.PAD
    # assert fillna('ffill', n=4) == FillnaMethodType.FFILL


def test_wrong_fillna_param():
    pass
    # wrong value
    # with pytest.raises(PrismValueError):
    #     assert fillna("Bfill", n=4) == FillnaMethodType.BFILL

    # with pytest.raises(PrismValueError):
    #     assert fillna("fill_zero", n=4)

    # # fillna() should only have one argument for either specifying a value or a method to fill the missing values
    # with pytest.raises(PrismValueError):
    #     assert fillna(value="1", method='bfill') == FillnaMethodType.BFILLs

    # # wrong type
    # with pytest.raises(PrismTypeError):
    #     assert fillna(method=123, n=4)


@_validate_args
def fill(
        method: str,
        n: int = 0,
        value=None) -> FillnaMethodType:
    return method


def test_fill_param():
    # check type
    # assert isinstance(fill('backfill', n=1), FillnaMethodType)

    # valid fill param
    assert fill('backfill', n=5) == FillnaMethodType.BACKFILL
    assert fill('bfill', n=6) == FillnaMethodType.BFILL
    assert fill('pad', n=7) == FillnaMethodType.PAD
    assert fill('ffill', n=8) == FillnaMethodType.FFILL


def test_wrong_fill_param():
    # wrong value
    with pytest.raises(Exception):
        assert fill("back fill", n=4) == FillnaMethodType.BACKFILL

    # with pytest.raises(Exception):
    #     assert fill(" ", n=4)

    # fill() can have argument value and method
    assert fill(value="1", method='bfill') == FillnaMethodType.BFILL

    # wrong type
    with pytest.raises(Exception):
        assert fill(method=1, n=4)
