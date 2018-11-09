import enum

import pandas as pd
import numpy as np
from uncertainties import ufloat

from uncertain_panda.utils.numerics import calculate_binomial_uncertainty
from .bootstrapper import bootstrap


class UncertaintyMode(enum.Enum):
    bootstrapping = "bootstrapping"
    binomial = "binomial"
    none = "none"


def calculate_with_uncertainty(df, *args, f, mode, bootstrapping_parameters=None, **kwargs):
    if bootstrapping_parameters is None:
        bootstrapping_parameters = {}

    if mode == UncertaintyMode.bootstrapping:
        value = f(df, *args, **kwargs)
        bootstrapped_values = bootstrap(df, *args, f=f, **kwargs, **bootstrapping_parameters)
        std = bootstrapped_values.std()
        return ufloat(value, std)

    elif mode == UncertaintyMode.binomial:
        n = df.count()
        k = df.sum()
        binomial_uncertainty = calculate_binomial_uncertainty(k, n)
        return ufloat(k / n, binomial_uncertainty)

    elif mode == UncertaintyMode.none:
        value = f(df, *args, **kwargs)
        return ufloat(value, np.NaN)

    raise NotImplementedError(mode)


def calculate_with_asymmetric_uncertainty(df, *args, f, mode, bootstrapping_parameters=None, **kwargs):
    if bootstrapping_parameters is None:
        bootstrapping_parameters = {}

    if mode == UncertaintyMode.bootstrapping:
        value = f(df, *args, **kwargs)
        bootstrapped_values = bootstrap(df, *args, f=f, **kwargs, **bootstrapping_parameters)

        # TODO: magic numbers
        return_dict = {f"{f.key}": value,
                       f"{f.key}_std_dev_left": value - np.percentile(bootstrapped_values, 31.7310508 / 2),
                       f"{f.key}_std_dev_right": np.percentile(bootstrapped_values, 100 - 31.7310508 / 2) - value}

    elif mode == UncertaintyMode.binomial:
        n = df.count()
        k = df.sum()
        binomial_uncertainty = calculate_binomial_uncertainty(k, n)

        return_dict = {"efficiency": k / n,
                       "efficiency_std_dev_left": binomial_uncertainty,
                       "efficiency_std_dev_right": binomial_uncertainty}

    elif mode == UncertaintyMode.none:
        value = f(df, *args, **kwargs)

        return_dict = {f"{f.key}": value, f"{f.key}_std_dev_left": np.NaN, f"{f.key}_std_dev_right": np.NaN}

    else:
        raise NotImplementedError(mode)

    return pd.Series(return_dict)


