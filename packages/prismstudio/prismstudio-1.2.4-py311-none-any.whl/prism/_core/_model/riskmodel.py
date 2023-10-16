import copy
import uuid

from ..._common.const import FrequencyType
from ..._prismcomponent.prismcomponent import _PrismModelComponent, _PrismComponent, _functioncomponent_builder
from ..._utils import _validate_args


_data_category = __name__.split(".")[-1]


class _PrismRiskModelComponent(_PrismModelComponent):
    _component_category_repr  = _data_category

    # def inv(self):
    #     return _functioncomponent_builder("inv", {}, self)

    def __getattribute__(self, name):
        if name not in [
            "get_data",
            "inv",
            "save",
            "copy",
            "query",
            "component_type",
            "categoryid",
            "component_category",
            "componentid",
            "component_name",
            "_query",
            "_dict_to_tree",
            "__class__",
        ]: raise AttributeError(f"{name} not allowed")
        return _PrismModelComponent.__getattribute__(self, name)


class qis(_PrismRiskModelComponent):
    r"""
    | Provides fast and accurate estimators of the covariance matrix based on nonlinear shrinkage for financial assets.
    | Nonlinear shrinkage derived under Frobenius loss and its two cousins, Inverse Stein's loss and Minimum Variance loss, called quadratic-inverse shrinkage (QIS).

    Parameters
    ----------

        frequency : str
            | Desired rebalancing frequency for the risk model
            | Examples:
            |     'M': Generates risk models at the end of every month.
            |     'M-23': Generates risk models on the 23rd day of each month.
            |     'W-M': Generates risk models every Monday of a week.

        period : int
            | Desired number of days (not business days) of data used to calculate a risk model.
            | Please note that the parameter value indicates the time frame covered and not the count of individual data samples.
            | For example, if you input 365 into the parameter, the risk model will be computed using all available data spanning a 365-day period.

        include : bool, default False
            | Determines whether to include pricing data from the rebalancing dates when calculating the risk model. By default, this parameter is set to False

    Returns
    -------
        prism._PrismComponent

    References
    ----------
        Ledoit, O. and Wolf, M. (2022). Quadratic shrinkage for large covariance matrices. Bernoulli.
        Available online at https://www.econ.uzh.ch/en/people/faculty/wolf/publications.html.

    Examples
    --------
        >>> qis = prism.riskmodel.qis("M", 252, False)
        >>> qis.get_data("KR_primary_prism", "2021-01-01", "2021-03-01")
        {'2021-01-31':
        31780818     690828765   682359177   693900517    31780641
        31780818      0.004068    0.000184    0.000325    0.000175    0.000279
        690828765     0.000184    0.001945    0.000134    0.000088    0.000066
        682359177     0.000325    0.000134    0.003783    0.000366    0.000118
        693900517     0.000175    0.000088    0.000366    0.002984   -0.000014
        31780641      0.000279    0.000066    0.000118   -0.000014    0.002087
        ...                ...         ...         ...         ...         ...
        571967822    -0.000072    0.000022    0.000013    0.000032   -0.000020
        31781107      0.000383    0.000077    0.000218    0.000144    0.000156
        681409416     0.000077    0.000031    0.000054    0.000055    0.000035
        683275334     0.000112    0.000056    0.000181    0.000047    0.000059
        1830288132    0.000067    0.000024    0.000114    0.000068    0.000038

                     670416042   650332107   670444531   689898516   133365196  ...
        31780818      0.000403    0.000079    0.000072    0.000782    0.000056  ...
        690828765    -0.000055    0.000043    0.000060    0.000436    0.000134  ...
        682359177     0.000177    0.000419    0.000199    0.000535    0.000429  ...
        693900517     0.000101    0.000297    0.000358    0.000207    0.000228  ...
        31780641      0.000183    0.000090    0.000059    0.000269    0.000051  ...
        ...                ...         ...         ...         ...         ...  ...
        571967822    -0.000041    0.000013    0.000020    0.000052    0.000048  ...
        31781107      0.000175    0.000069    0.000060    0.000305    0.000043  ...
        681409416     0.000037    0.000029    0.000039    0.000074    0.000016  ...
        683275334     0.000077    0.000053    0.000024    0.000224    0.000048  ...
        1830288132    0.000031    0.000042    0.000042    0.000065    0.000031  ...
        }
    """

    @_validate_args
    def __init__(
        self,
        frequency: str,
        sample_period: str,
        include: bool = False,
    ):
        super().__init__(
            frequency=frequency,
            sample_period=sample_period,
            include=include,
        )


def map_attribute(self, attribute):
    attributes = self.attributes[attribute]
    ret = self.copy()
    ret.column = attributes
    ret.index = attributes
    return ret
