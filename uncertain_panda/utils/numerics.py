from functools import partial

import numpy as np
import pandas as pd

ONE_SIGMA = 31.7310508


def pandas_coverage(df, cl=0.68):
    if isinstance(df, pd.DataFrame):
        return df.apply(partial(coverage, cl=cl))
    else:
        return coverage(df, cl=cl)


def value_counts(df, *args, normalize=False, **kwargs):
    possible_values = set(df)
    normalization = len(df)

    if normalize:
        normalization = 1

    count = {
        val: (df == val).unc.mean(*args, **kwargs) * normalization
        for val in possible_values
    }
    return pd.Series(count, index=pd.CategoricalIndex(possible_values))


def coverage(series, cl=0.68):
    series = series[~np.isnan(series)]

    if len(series) == 0:
        return np.NAN  # pragma: no cover

    centered_dist = np.abs(series - np.median(series))
    b = np.percentile(centered_dist, 100 * cl)
    return b
