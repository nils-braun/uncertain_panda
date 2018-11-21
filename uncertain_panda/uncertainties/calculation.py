import enum

from .bootstrap_result import BootstrapResult
from .calculators import bootstrap, calculate_binomial_uncertainty

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from uncertainties.core import Variable


class UncertaintyMode(enum.Enum):
    bootstrapping = "uncertainties"
    binomial = "binomial"


def _calculate_value(df, *args, f, **kwargs):
    """
    Internal helper function for applying f on a data frame/series etc.
    without the bootstrapping parameters.
    """
    kwargs.pop("number_of_draws", None)
    kwargs.pop("chunks", None)
    kwargs.pop("pandas", None)

    return f(df, *args, **kwargs)


def create_uncertainty(df, *args, f, mode, **kwargs):
    value = _calculate_value(df, *args, f=f, **kwargs)

    if mode == UncertaintyMode.bootstrapping:
        bootstrapped_values = bootstrap(df, *args, f=f, **kwargs)
        return BootstrapResult(value, bootstrapped_values)

    elif mode == UncertaintyMode.binomial:
        uncertainty = calculate_binomial_uncertainty(df)
        return Variable(value, uncertainty)

    raise NotImplementedError(mode)
