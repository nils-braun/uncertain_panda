from unittest import TestCase

import numpy as np

from uncertain_panda import pandas as pd
from uncertain_panda.bootstrapping.calculation import UncertaintyMode
from uncertain_panda.bootstrapping.functions import NonNanNumpyFunction

NUM_SAMPLES = 100
NUM_COLUMNS = 3


class AsymPandasMethodsTestCase(TestCase):
    def assertCorrectOutput(self, df):
        self.assertEqual(df.shape, (NUM_COLUMNS, 3))

    def test_asym_df_functions(self):
        df = pd.DataFrame({i: np.random.rand(NUM_SAMPLES) for i in range(NUM_COLUMNS)})

        self.assertCorrectOutput(df.calculate_with_asymmetric_uncertainty(f=NonNanNumpyFunction("mean")))
        self.assertCorrectOutput(df.calculate_with_asymmetric_uncertainty(mode=UncertaintyMode.binomial))

