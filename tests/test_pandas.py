from unittest import TestCase

import numpy as np

from uncertain_panda import pandas as pd
from uncertain_panda.bootstrapping.calculation import UncertaintyMode
from uncertain_panda.bootstrapping.functions import NonNanNumpyFunction

NUM_SAMPLES = 100
NUM_COLUMNS = 3


class BasicPandasMethodsTestCase(TestCase):
    def assertCorrectOutput(self, df):
        self.assertEqual(df.shape, (NUM_COLUMNS,))

    def test_basic_df_functions(self):
        df = pd.DataFrame({i: np.random.rand(NUM_SAMPLES) for i in range(NUM_COLUMNS)})

        self.assertCorrectOutput(df.mean_with_uncertainty())
        self.assertCorrectOutput((df < 0.5).efficiency_with_uncertainty())
        self.assertCorrectOutput(df.std_with_uncertainty())
        self.assertCorrectOutput(df.coverage_with_uncertainty())
        self.assertCorrectOutput(df.coverage())
        self.assertCorrectOutput(df.coverage_with_uncertainty(0.8))
        self.assertCorrectOutput(df.coverage(0.8))

        (df[0] > 0.5).value_counts_with_uncertainty()
        (df[0] > 0.5).value_counts_with_uncertainty(normalize=True)

        df = pd.concat([df.mean_with_uncertainty(), df.std_with_uncertainty()], axis=1)
        self.assertEqual(df.shape, (NUM_COLUMNS, 2))
        self.assertEqual(df.nominal_value.shape, (NUM_COLUMNS, 2))
        self.assertEqual(df.std_dev.shape, (NUM_COLUMNS, 2))

    def test_without_uncertainty(self):
        df = pd.DataFrame({i: np.random.rand(NUM_SAMPLES) for i in range(NUM_COLUMNS)})

        df_uncertainty = df.mean_with_uncertainty()
        df_no_uncertainty = df.calculate_with_uncertainty(f=NonNanNumpyFunction("mean"), mode=UncertaintyMode.none)
        pd.testing.assert_series_equal(df_uncertainty.nominal_value, df_no_uncertainty.nominal_value, check_names=False)

        df_no_uncertainty = df.calculate_with_asymmetric_uncertainty(f=NonNanNumpyFunction("mean"), mode=UncertaintyMode.none)
        pd.testing.assert_series_equal(df_uncertainty.nominal_value, df_no_uncertainty["mean"], check_names=False)
