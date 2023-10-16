import pytest

from prism._common.const import FinancialPreliminaryType, FinancialPeriodType as _PeriodType
from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def get_balance_sheet(
        preliminary: FinancialPreliminaryType,
        universe=None,
        dataitemid: int = 1,
        periodtype: _PeriodType = 'A',
        engine=None,
        offset: int = 365,
        n_quarter: int = 1,
        currency: str = 'trade') -> FinancialPreliminaryType:
    """
    valid argument:
        'keep', 'ignore', 'drop', 'null'
    """
    return preliminary


def test_preliminary_param():
    assert get_balance_sheet(preliminary=None) is None
    assert get_balance_sheet(universe='S&P 500', dataitemid=101, periodtype='A',
                             engine=None, offset=180, n_quarter=1, preliminary='keep', currency='trade') == FinancialPreliminaryType.KEEP

    # check type
    # assert isinstance(get_balance_sheet(preliminary='keep'), FinancialPreliminaryType)

    # valid preliminary param
    assert get_balance_sheet(
        preliminary='keep') == FinancialPreliminaryType.KEEP
    assert get_balance_sheet(
        preliminary='ignore') == FinancialPreliminaryType.IGNORE
    assert get_balance_sheet(
        preliminary='drop') == FinancialPreliminaryType.DROP
    assert get_balance_sheet(
        preliminary='null') == FinancialPreliminaryType.NULL


def test_wrong_preliminary_param():
    # wrong value
    with pytest.raises(Exception):
        assert get_balance_sheet(
            preliminary="KEEP") == FinancialPreliminaryType.KEEP

    with pytest.raises(Exception):
        assert get_balance_sheet(preliminary="do sth")

    # wrong type
    with pytest.raises(Exception):
        assert get_balance_sheet(preliminary=1)
