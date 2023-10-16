import numbers

from prism._utils.exceptions import PrismTypeError as _PrismTypeError

from .._common.const import SPECIALVALUEMAP as _SPECIALVALUEMAP
from .._prismcomponent.prismcomponent import _PrismComponent, _PrismValue, _functioncomponent_builder
from .._prismcomponent.abstract_prismcomponent import _AbstractPrismComponent
from .._utils import _validate_args


__all__ = [
    "n_periods_beta",
    "n_periods_intercept",
    "n_periods_residual",
    "cross_sectional_beta",
    "cross_sectional_intercept",
    "cross_sectional_residual"
]


def _fn_builder(component_name, component_args, cmpts):
    cmpts_ = []
    for c in cmpts:
        if isinstance(c, _PrismComponent):
            cmpts_.append(c)
        elif isinstance(c, numbers.Real):
            other = _SPECIALVALUEMAP.get(other, other)
            cmpts_.append(_PrismValue(data=c))
        else:
            raise _PrismTypeError(f"Incompatible type for {component_name}: {type(c)}")

    return _functioncomponent_builder(component_name, component_args, *cmpts_)


@_validate_args
def n_periods_beta(x: _AbstractPrismComponent, y: _AbstractPrismComponent, n: int, min_periods: int = 1, fit_intercept: bool = True):
    """
    Beta coefficient in ordinary least squares simple linear regression.

    Parameters
    ----------
        x : PrismComponent
            Independent variable

        y : PrismComponent
            Dependent variable

        n : int
            Number of data points from the independent and dependent time series to include in the regression

        min_periods : int, default 1
            Minimum number of observations in window required to have a value; otherwise, result is ``np.nan``.

        fit_intercept : bool, default True
            Whether to calculate the intercept for the regression. If False, no intercept will be used in calculations (i.e. data is expected to be centered).

    Returns
    -------
        prism._PrismComponent
            Resampled timeseries of the PrismComponent.

    Examples
    --------
        >>> cash_flow = prism.financial.cash_flow(dataitemid=100513, periodtype='LTM', preliminary='ignore', currency='trade')
        >>> cash_flow_daily = close.resample("D", 365)
        >>> returns_daily = prism.market.close().n_periods_pct_change(1).resample("D", 365)
        >>> beta = prism.ols.n_periods_beta(cash_flow_daily, returns_daily, 252, 150)
        >>> beta.get_data(universe='Korea_primary', startdate='2010-01-01', enddate='2011-01-01')
                listingid	       date         value
        0         2666983  2010-01-01  6.596677e-09
        1         2666983  2010-01-02  6.573793e-09
        2         2666983  2010-01-03  6.551399e-09
        3         2666983  2010-01-04  6.769521e-09
        4         2666983  2010-01-05  6.746380e-09
        ...           ...         ...           ...
        619136  306481998  2010-12-28           NaN
        619137  306481998  2010-12-29           NaN
        619138  306481998  2010-12-30           NaN
        619139  306481998  2010-12-31           NaN
        619140  306481998  2011-01-01           NaN
    """
    return _fn_builder(
        "n_periods_beta",
        {"n": n, "min_periods": min_periods, "fit_intercept": fit_intercept},
        [x, y]
    )


@_validate_args
def n_periods_intercept(x: _AbstractPrismComponent, y: _AbstractPrismComponent, n: int, min_periods=1):
    """
    Residual for ordinary least squares simple linear regression

    Parameters
    ----------
        x : PrismComponent
            Independent variable

        y : PrismComponent
            Dependent variable

        n : int
            Number of data points from the independent and dependent time series to include in the regression

        min_periods : int, default 1
            Minimum number of observations in window required to have a value; otherwise, result is ``np.nan``.

    Returns
    -------
        prism._PrismComponent
            Resampled timeseries of the PrismComponent.

    Examples
    --------
        >>> cash_flow = prism.financial.cash_flow(dataitemid=100513, periodtype='LTM', preliminary='ignore', currency='trade')
        >>> cash_flow_daily = close.resample("D", 365)
        >>> returns_daily = prism.market.close().n_periods_pct_change(1).resample("D", 365)
        >>> intercept = prism.ols.n_periods_intercept(cash_flow_daily, returns_daily, 252, 150)
        >>> intercept.get_data(universe='Korea_primary', startdate='2010-01-01', enddate='2011-01-01')
                listingid	       date     value
        0         2666983  2010-01-01  0.016087
        1         2666983  2010-01-02  0.016010
        2         2666983  2010-01-03  0.015933
        3         2666983  2010-01-04  0.017095
        4         2666983  2010-01-05  0.016844
        ...           ...         ...       ...
        619136  306481998  2010-12-28       NaN
        619137  306481998  2010-12-29       NaN
        619138  306481998  2010-12-30       NaN
        619139  306481998  2010-12-31       NaN
        619140  306481998  2011-01-01       NaN
    """
    return _fn_builder(
        "n_periods_intercept",
        {"n": n, "min_periods": min_periods},
        [x, y]
    )


@_validate_args
def n_periods_residual(x: _AbstractPrismComponent, y: _AbstractPrismComponent, n: int, min_periods: int = 1, fit_intercept: bool = True):
    """
    Intercept in ordinary least squares simple linear regression.

    Parameters
    ----------
        x : PrismComponent
            Independent variable

        y : PrismComponent
            Dependent variable

        n : int
            Number of data points from the independent and dependent time series to include in the regression

        min_periods : int, default 1
            Minimum number of observations in window required to have a value; otherwise, result is ``np.nan``.

        fit_intercept : bool, default True
            Whether to calculate the intercept for the regression. If False, no intercept will be used in calculations (i.e. data is expected to be centered).

    Returns
    -------
        prism._PrismComponent
            Resampled timeseries of the PrismComponent.


    Examples
    --------
        >>> cash_flow = prism.financial.cash_flow(dataitemid=100513, periodtype='LTM', preliminary='ignore', currency='trade')
        >>> cash_flow_daily = close.resample("D", 365)
        >>> returns_daily = prism.market.close().n_periods_pct_change(1).resample("D", 365)
        >>> residual = prism.ols.n_periods_residual(cash_flow_daily, returns_daily, 252, 150)
        >>> residual.get_data(universe='Korea_primary', startdate='2010-01-01', enddate='2011-01-01')
                listingid	       date      value
        0         2666983  2010-01-01  -0.009541
        1         2666983  2010-01-02  -0.009664
        2         2666983  2010-01-03  -0.009787
        3         2666983  2010-01-04  -0.000018
        4         2666983  2010-01-05  -0.000230
        ...           ...         ...        ...
        619136  306481998  2010-12-28        NaN
        619137  306481998  2010-12-29        NaN
        619138  306481998  2010-12-30        NaN
        619139  306481998  2010-12-31        NaN
        619140  306481998  2011-01-01        NaN
    """
    return _fn_builder(
        "n_periods_residual",
        {"n": n, "min_periods": min_periods, "fit_intercept": fit_intercept},
        [x, y]
    )


@_validate_args
def cross_sectional_beta(x: _AbstractPrismComponent, y: _AbstractPrismComponent, fit_intercept: bool = True):
    """
    Beta coefficient in ordinary least squares simple linear regression.

    Parameters
    ----------
        x : PrismComponent
            Independent variable

        y : PrismComponent
            Dependent variable

        fit_intercept : bool, default True
            Whether to calculate the intercept for the regression. If False, no intercept will be used in calculations (i.e. data is expected to be centered).

    Returns
    -------
        prism._PrismComponent
            Resampled timeseries of the PrismComponent.

    """
    return _fn_builder(
        "cross_sectional_beta",
        {"fit_intercept": fit_intercept},
        [x, y]
    )


@_validate_args
def cross_sectional_intercept(x: _AbstractPrismComponent, y: _AbstractPrismComponent):
    """
    Intercept in ordinary least squares simple linear regression

    Parameters
    ----------
        x : PrismComponent
            Independent variable

        y : PrismComponent
            Dependent variable

    Returns
    -------
        prism._PrismComponent
            Resampled timeseries of the PrismComponent.

    """
    return _fn_builder(
        "cross_sectional_intercept",
        {},
        [x, y]
    )


@_validate_args
def cross_sectional_residual(x: _AbstractPrismComponent, y: _AbstractPrismComponent, fit_intercept: bool = True):
    """
    Residual for ordinary least squares simple linear regression.

    Parameters
    ----------
        x : PrismComponent
            Independent variable

        y : PrismComponent
            Dependent variable

        fit_intercept : bool, default True
            Whether to calculate the intercept for the regression. If False, no intercept will be used in calculations (i.e. data is expected to be centered).

    Returns
    -------
        prism._PrismComponent
            Resampled timeseries of the PrismComponent.
    """
    return _fn_builder(
        "cross_sectional_residual",
        {"fit_intercept": fit_intercept},
        [x, y]
    )