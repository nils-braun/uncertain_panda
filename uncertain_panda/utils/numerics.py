from functools import partial

import numpy as np
import pandas as pd


def pandas_coverage(df, cl=0.68):
    if isinstance(df, pd.DataFrame):
        return df.apply(partial(coverage, cl=cl))
    else:
        return coverage(df, cl=cl)


def coverage(series, cl=0.68):
    series = series[~np.isnan(series)]

    if len(series) == 0:
        return np.NAN

    centered_dist = np.abs(series - np.median(series))
    b = np.percentile(centered_dist, 100*cl)
    return b
