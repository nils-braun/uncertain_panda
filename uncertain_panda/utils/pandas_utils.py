import pandas as pd


def band(x, cl=0.9):
    return pd.Series({"median_std_dev_left": x.median() - x.quantile((1 - cl) / 2),
                      "median_std_dev_right": x.quantile((1 + cl) / 2) - x.median(),
                      "median": x.median()
                      })

def value_counts_with_uncertainty(series, normalize=False):
    possible_values = set(series)

    normalization = len(series)
    if normalize:
        normalization = 1

    count = {
        val: (series == val).mean_with_uncertainty() * normalization
        for val in possible_values
    }

    return pd.Series(count, index=pd.CategoricalIndex(possible_values))

