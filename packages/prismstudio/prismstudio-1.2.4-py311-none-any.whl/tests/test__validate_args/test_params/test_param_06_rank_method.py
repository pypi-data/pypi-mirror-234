from typing import Union

import pytest

from prism._common.const import RankType
from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def factor_backtest(
        self,
        jobname: Union[str, list] = None,
        report: bool = True,
        frequency: str = None,
        bins: int = None,
        rank_method: str = None) -> RankType:
    """
    valid arguments:
        'standard', 'modified', 'dense', 'ordinal', 'fractional'
    """
    return rank_method


def test_periodtype_param():
    assert factor_backtest(None) is None
    assert factor_backtest(
        None, jobname=["job1", "job2"], rank_method="standard", frequency='N', bins=1) == RankType.STANDARD

    # check type
    assert isinstance(factor_backtest(None, "job", rank_method="standard"), RankType)

    # valid periodtype param
    assert factor_backtest(
        None, "job", rank_method="standard") == RankType.STANDARD
    assert factor_backtest(
        None, "job", rank_method="modified") == RankType.MODIFIED
    assert factor_backtest(
        None, "job", rank_method="dense") == RankType.DENSE
    assert factor_backtest(
        None, "job", rank_method="ordinal") == RankType.ORDINAL
    assert factor_backtest(
        None, "job", rank_method="fractional") == RankType.FRACTIONAL


def test_wrong_periodtype_param():
    # wrong value
    with pytest.raises(PrismValueError):
        assert factor_backtest(None, "job1", rank_method='annual')

    with pytest.raises(PrismValueError):
        assert factor_backtest(
            None, "job1", rank_method='Standard') == RankType.STANDARD

    # wrong type
    with pytest.raises(PrismTypeError):
        assert factor_backtest(None, "job", rank_method=1)

    with pytest.raises(PrismTypeError):
        assert factor_backtest(
            None, "job", rank_method='standard', frequency=1) == RankType.STANDARD
