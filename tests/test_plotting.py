from unittest import TestCase

import numpy as np

from uncertain_panda import pandas as pd
from matplotlib import pyplot as plt

from uncertain_panda.bootstrapping.functions import NonNanNumpyFunction

plt.switch_backend("pdf")

NUM_SAMPLES = 100
NUM_COLUMNS = 3


class BasicPlottingMethodsTestCase(TestCase):
    def test_basic_plotting_functions(self):
        df = pd.DataFrame({i: np.random.rand(NUM_SAMPLES) for i in range(NUM_COLUMNS)})

        df.plot_with_uncertainty()
        df.plot_with_uncertainty(kind="bar")

        df_uncertainty = df.mean_with_uncertainty()

        df_uncertainty.plot_with_uncertainty()
        df_uncertainty.plot_with_uncertainty(kind="bar")

        df_uncertainty = df.calculate_with_asymmetric_uncertainty(f=NonNanNumpyFunction("mean"))
        print(df_uncertainty)
        df_uncertainty.plot_with_uncertainty(key="mean")





