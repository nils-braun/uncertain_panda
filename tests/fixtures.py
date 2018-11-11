from unittest import TestCase

import numpy as np


class UncertainPandaTestCase(TestCase):
    def setUp(self):
        super().setUp()

        np.random.seed(0)

    def assertNear(self, actual, should, deviation=0.1):
        self.assertLess(abs(actual - should), deviation)