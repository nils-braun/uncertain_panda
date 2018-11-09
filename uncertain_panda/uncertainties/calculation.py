import enum

import pandas as pd
import numpy as np
from uncertainties import ufloat

from ..utils.numerics import ONE_SIGMA
from .calculators import bootstrap, calculate_binomial_uncertainty


class UncertaintyMode(enum.Enum):
    bootstrapping = "uncertainties"
    binomial = "binomial"
    none = "none"


def _calculate_value(df, *args, f, mode, **kwargs):
    kwargs.pop("number_of_draws", None)
    kwargs.pop("chunks", None)
    kwargs.pop("pandas", None)

    if mode in [UncertaintyMode.bootstrapping, UncertaintyMode.none]:
        return f(df, *args, **kwargs)

    elif mode == UncertaintyMode.binomial:
        n = df.count()
        k = df.sum()
        return k / n

    raise NotImplementedError(mode)


def calculate_with_uncertainty(df, *args, f, mode, **kwargs):
    value = _calculate_value(df, *args, f=f, mode=mode, **kwargs)

    if mode == UncertaintyMode.bootstrapping:
        bootstrapped_values = bootstrap(df, *args, f=f, **kwargs)
        uncertainty = bootstrapped_values.std()
        return ufloat(value, uncertainty)

    elif mode == UncertaintyMode.binomial:
        uncertainty = calculate_binomial_uncertainty(df)
        return ufloat(value, uncertainty)

    elif mode == UncertaintyMode.none:
        return ufloat(value, np.NaN)

    raise NotImplementedError(mode)


def calculate_with_asymmetric_uncertainty(df, *args, f, mode, **kwargs):
    value = _calculate_value(df, *args, f=f, mode=mode, **kwargs)
    return_dict = {f"{f.key}": value}

    if mode == UncertaintyMode.bootstrapping:
        bootstrapped_values = bootstrap(df, *args, f=f, **kwargs)
        # TODO: magic numbers
        return_dict[f"{f.key}_std_dev_left"] = value - np.percentile(bootstrapped_values, ONE_SIGMA / 2)
        return_dict[f"{f.key}_std_dev_right"] = np.percentile(bootstrapped_values, 100 - ONE_SIGMA / 2) - value

    elif mode == UncertaintyMode.binomial:
        binomial_uncertainty = calculate_binomial_uncertainty(df)

        return_dict[f"{f.key}_std_dev_left"] = binomial_uncertainty
        return_dict[f"{f.key}_std_dev_right"] = binomial_uncertainty

    elif mode == UncertaintyMode.none:
        return_dict[f"{f.key}_std_dev_left"] = np.NaN
        return_dict[f"{f.key}_std_dev_right"] = np.NaN

    else:
        raise NotImplementedError(mode)

    return pd.Series(return_dict)


