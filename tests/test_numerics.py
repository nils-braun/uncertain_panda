from uncertain_panda import pandas as pd

import numpy as np

from tests.fixtures import UncertainPandaTestCase


class TestNumerics(UncertainPandaTestCase):

    def test_coverage_normal(self):
        for sigma in [1, 5, 100]:
            df = pd.Series(np.random.normal(np.random.randint(-10, 10), sigma, 2000))
            coverage = df.coverage(0.68)

            # We allow for +- 5% deviation
            self.assertGreater(coverage, 0.95 * sigma)
            self.assertLess(coverage, 1.05 * sigma)

    def test_coverage_uniform(self):
        df = pd.Series(10 * np.random.rand(10000))

        # We also allow for a small deviation here
        self.assertLess(abs(df.coverage(1.0) - 5), 0.1)
        self.assertLess(abs(df.coverage(0.5) - 2.5), 0.1)
        self.assertLess(abs(df.coverage(0.2) - 1.0), 0.1)

    def test_dataframe_coverage(self):
        df = pd.DataFrame({"a": np.random.normal(np.random.randint(-10, 10), 5, 2000),
                           "b": np.random.normal(np.random.randint(-10, 10), 5, 2000)})

        coverage = df.coverage(0.68)
        self.assertLess(abs(coverage["a"] - 5), 0.5)
        self.assertLess(abs(coverage["b"] - 5), 0.5)
