import numpy as np
import pandas as pd


def bootstrap(df, *args, f, number_of_draws=250, chunks=1000, pandas=True, **kwargs):
    if len(df) == 0:
        return pd.Series([])

    if pandas:
        measurement_results = pd.Series(
            [f(df.sample(frac=1.0, replace=True), *args, **kwargs) for _ in range(number_of_draws)])
    else:
        from dask import array as da

        # First, draw <number_of_draws> times randomly from the full dataset
        # to simulate different measurements
        random_draws = da.random.choice(df, chunks=chunks, size=(number_of_draws, len(df)), replace=True)

        # Then, apply the function f on all the measurements
        measurement_results = f.call_on_dask_array(random_draws, *args, **kwargs)

    return measurement_results


def calculate_binomial_uncertainty(df):
    n = df.count()
    k = df.sum()
    return np.sqrt((k + 1) * (k + 2) / (n + 2) / (n + 3) - (k + 1) ** 2 / (n + 2) ** 2)