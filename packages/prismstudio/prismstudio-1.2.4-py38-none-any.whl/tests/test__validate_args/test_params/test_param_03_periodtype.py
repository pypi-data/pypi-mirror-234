import pytest

from prism._common.const import EstimatePeriodType as _PeriodType
from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def consensus(
    dataitemid: int,
    periodtype: _PeriodType,
    periodout: int = 0,
    currency: str = 'trade',
) -> _PeriodType:
    """
    valid periodtype =
        'Annual', 'A', 'Semi-Annual', 'SA', 'Quarterly', 'Q', 'YTD', 'LTM', 'Non-Periodic', 'NTM', 'Q-SA'
    """
    return periodtype


def test_periodtype_param():
    pass
    # assert consensus(0, 'Annual', 0, 'trade') == _PeriodType.ANNUAL

    # # check type
    # assert isinstance(consensus(0, 'Annual', 0, 'trade'), _PeriodType)

    # # valid periodtype param
    # assert consensus(1, 'Annual') == _PeriodType.ANNUAL
    # assert consensus(2, 'A') == _PeriodType.A
    # assert consensus(3, 'Semi-Annual') == _PeriodType.SEMI_ANNUAL
    # assert consensus(4, 'SA') == _PeriodType.SA
    # assert consensus(5, 'Quarterly') == _PeriodType.QUARTERLY
    # assert consensus(6, 'Q') == _PeriodType.Q
    # assert consensus(7, 'YTD') == _PeriodType.YTD
    # assert consensus(8, 'LTM') == _PeriodType.LTM
    # assert consensus(9, 'Non-Periodic') == _PeriodType.NON_PERIODIC
    # assert consensus(10, 'NTM') == _PeriodType.NTM
    # assert consensus(11, 'Q-SA') == _PeriodType.QSA

    # assert consensus(1, periodtype='Annual') == _PeriodType.ANNUAL
    # assert consensus(2, periodtype='A') == _PeriodType.A
    # assert consensus(3, periodtype='Semi-Annual') == _PeriodType.SEMI_ANNUAL
    # assert consensus(4, periodtype='SA') == _PeriodType.SA
    # assert consensus(5, periodtype='Quarterly') == _PeriodType.QUARTERLY
    # assert consensus(6, periodtype='Q') == _PeriodType.Q
    # assert consensus(7, periodtype='YTD') == _PeriodType.YTD
    # assert consensus(8, periodtype='LTM') == _PeriodType.LTM
    # assert consensus(9, periodtype='Non-Periodic') == _PeriodType.NON_PERIODIC
    # assert consensus(10, periodtype='NTM') == _PeriodType.NTM
    # assert consensus(11, periodtype='Q-SA') == _PeriodType.QSA


def test_wrong_periodtype_param():
    pass
    # wrong value
    # with pytest.raises(PrismValueError):
    #     assert consensus(1, 'annual') == _PeriodType.ANNUAL

    # with pytest.raises(PrismValueError):
    #     assert consensus(1, 'a') == _PeriodType.A

    # with pytest.raises(PrismValueError):
    #     assert consensus(1, 'typo period')

    # with pytest.raises(PrismValueError):
    #     assert consensus(1, 'q-SA') == _PeriodType.QSA

    # # wrong type
    # with pytest.raises(PrismTypeError):
    #     assert consensus(1, periodtype=0, currency='won')

    # with pytest.raises(PrismTypeError):
    #     assert consensus(2, 0)

    # with pytest.raises(PrismTypeError):
    #     assert consensus(3, 'Annual', '0') == _PeriodType.ANNUAL
