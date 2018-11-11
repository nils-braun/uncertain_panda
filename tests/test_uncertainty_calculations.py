from uncertain_panda import pandas as pd
import numpy as np
from uncertainties.core import Variable

from tests.fixtures import UncertainPandaTestCase


class TestUncertaintyCalculations(UncertainPandaTestCase):
    def test_shape(self):
        some_functions = ["mean", "median"]

        N = 10

        series = pd.Series(np.random.rand(N))
        df = pd.DataFrame({"a": np.random.rand(N), "b": np.random.rand(N)})
        df_grouped = pd.DataFrame({"a": np.random.choice([1, 2, 3], N), "b": np.random.rand(N),
                                   "c": np.random.rand(N), "d": np.random.rand(N)}).groupby("a")

        for f in some_functions:
            result = getattr(series.unc, f)()
            self.assertIsInstance(result, Variable)

            if f != "median":
                result = getattr(series.unc, f)(pandas=False)
                self.assertIsInstance(result, Variable)

            result = getattr(df.unc, f)()
            self.assertEqual(result.shape, (2,))
            self.assertIsInstance(result, pd.Series)

            if f != "median":
                result = getattr(df.unc, f)(pandas=False)
                self.assertEqual(result.shape, (2,))
                self.assertIsInstance(result, pd.Series)

            result = getattr(df_grouped.unc, f)()
            self.assertEqual(result.shape, (3, 4))
            self.assertIsInstance(result, pd.DataFrame)

            if f != "median":
                result = getattr(df_grouped.unc, f)(pandas=False)
                self.assertEqual(result.shape, (3, 4))
                self.assertIsInstance(result, pd.DataFrame)

    def test_mean(self):
        df = pd.Series(np.random.normal(10, 5, 2000))

        mean = df.unc.mean()
        self.assertNear(mean.nominal_value, 10, 0.2)
        self.assertNear(mean.std_dev, 5 / np.sqrt(2000), 0.1)

    def test_value_counts(self):
        df = pd.DataFrame({"a": [1] * 100 + [2] * 200 + [3] * 300,
                           "b": ["a"] * 100 + ["b"] * 200 + ["c"] * 300})

        value_counts = df.unc.value_counts()
        self.assertEqual(value_counts.shape, (6, 2))

        self.assertTrue((value_counts["a"].loc[[1, 2, 3]].nominal_value == [100, 200, 300]).all())
        self.assertTrue((value_counts["b"].loc[["a", "b", "c"]].nominal_value == [100, 200, 300]).all())

    def test_binomial_unc(self):
        df = pd.Series(np.random.choice([0, 1], size=1000, p=[0.3, 0.7]))

        result = df.unc.efficiency()
        result_mean = df.unc.mean()

        self.assertNear(result.nominal_value, 0.7)
        self.assertNear(result.std_dev, result_mean.std_dev)