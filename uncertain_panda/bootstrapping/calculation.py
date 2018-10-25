import enum

import pandas as pd
import numpy as np
from uncertainties import ufloat

from .bootstrapper import bootstrap


class UncertaintyMode(enum.Enum):
    bootstrapping = "bootstrapping"
    binomial = "binomial"
    none = "none"


def calculate_with_uncertainty(df, *args, f, mode=UncertaintyMode.bootstrapping, bootstrapping_parameters=None, **kwargs):
    if bootstrapping_parameters is None:
        bootstrapping_parameters = {}

    if df.__class__ == pd.DataFrame:
        return df.apply(lambda col: calculate_with_uncertainty(col, *args, f=f, mode=mode,
                                                               bootstrapping_parameters=bootstrapping_parameters, **kwargs))

    if mode == UncertaintyMode.bootstrapping:
        value = f(df, *args, **kwargs)
        bootstrapped_values = bootstrap(df, *args, f=f, bootstrapping_parameters=bootstrapping_parameters, **kwargs)
        std = bootstrapped_values.std()
        value_with_uncertainty = ufloat(value, std)

    elif mode == UncertaintyMode.binomial:
        n = df.count()
        k = df.sum()
        binomial_uncertainty = _calculate_binomial_uncertainty(k, n)
        value_with_uncertainty = ufloat(k / n, binomial_uncertainty)

    elif mode == UncertaintyMode.none:
        value = f(df, *args, **kwargs)
        value_with_uncertainty = ufloat(value, np.NaN)

    else:
        raise ValueError(mode)

    return value_with_uncertainty


def calculate_with_asymmetric_uncertainty(df, *args, f=None, mode=UncertaintyMode.bootstrapping, bootstrapping_parameters=None, **kwargs):
    if df.__class__ == pd.DataFrame:
        return df.apply(lambda col: calculate_with_asymmetric_uncertainty(col, *args, f=f, mode=mode,
                                                               bootstrapping_parameters=bootstrapping_parameters, **kwargs)).T

    if mode == UncertaintyMode.bootstrapping:
        value = f(df, *args, **kwargs)
        bootstrapped_values = bootstrap(df, *args, f=f, bootstrapping_parameters=bootstrapping_parameters, **kwargs)

        # TODO: magic numbers

        return_dict = {f"{f.key}": value,
                       f"{f.key}_std_dev_left": value - np.percentile(bootstrapped_values, 31.7310508 / 2),
                       f"{f.key}_std_dev_right": np.percentile(bootstrapped_values, 100 - 31.7310508 / 2) - value}

    elif mode == UncertaintyMode.binomial:
        n = df.count()
        k = df.sum()
        binomial_uncertainty = _calculate_binomial_uncertainty(k, n)

        return_dict = {"efficiency": k / n,
                       "efficiency_std_dev_left": binomial_uncertainty,
                       "efficiency_std_dev_right": binomial_uncertainty}

    elif mode == UncertaintyMode.none:
        value = f(df, *args, **kwargs)

        return_dict = {f"{f.key}": value, f"{f.key}_std_dev_left": np.NaN, f"{f.key}_std_dev_right": np.NaN}

    return pd.Series(return_dict)


def _calculate_binomial_uncertainty(k, n):
    return np.sqrt((k + 1) * (k + 2) / (n + 2) / (n + 3) - (k + 1) ** 2 / (n + 2) ** 2)
