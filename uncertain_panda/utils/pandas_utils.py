import pandas as pd


def band(x, cl=0.9):
    return pd.Series({"median_std_dev_left": x.median() - x.quantile((1 - cl) / 2),
                      "median_std_dev_right": x.quantile((1 + cl) / 2) - x.median(),
                      "median": x.median()
                      })

