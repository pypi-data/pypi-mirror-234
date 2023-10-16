import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def _get_price(
    universe: str,
    adjustment: str | bool,
    offset: int = 0,
    package: str = 'Prism Market',
    engine=None,
):
    """
    valid adjustment =
        'all', 'split', 'dividend', True, False
    """
    return True


def test_adjustment_param():
    assert _get_price('S&P 500', "all", offset=0, package='Prism Market')

    # valid adjustment param
    assert _get_price('S&P 500', "all")
    assert _get_price('S&P 500', "split")
    assert _get_price('S&P 500', "dividend")
    assert _get_price('S&P 500', True)
    assert _get_price('S&P 500', False)

    assert _get_price('S&P 500', adjustment="all")
    assert _get_price('S&P 500', adjustment="split")
    assert _get_price('S&P 500', adjustment="dividend")
    assert _get_price('S&P 500', adjustment=True)
    assert _get_price('S&P 500', adjustment=False)


def test_wrong_adjustment_param():
    pass
    # wrong value
    # with pytest.raises(PrismValueError):
    #     assert _get_price('S&P 500', 'alll')

    # with pytest.raises(PrismValueError):
    #     assert _get_price('S&P 500', 'SPLIT')

    # with pytest.raises(PrismValueError):
    #     assert _get_price('S&P 500', 'true')

    # # wrong type
    # with pytest.raises(PrismTypeError):
    #     assert _get_price('S&P 500', adjustment=0)

    # with pytest.raises(PrismTypeError):
    #     assert _get_price('S&P 500', True, offset='zero')

    # with pytest.raises(PrismTypeError):
    #     assert _get_price('S&P 500', False, '0')
