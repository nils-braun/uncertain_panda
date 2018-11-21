import pandas as pd

from ..utils.numerics import ONE_SIGMA

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from uncertainties.core import Variable


class BootstrapResult(Variable):
    def __init__(self, nominal_value, bootstrap):
        self._bootstrap = bootstrap

        super().__init__(nominal_value, self.bs().std())

    def bs(self):
        return self._bootstrap

    def ci(self, a=ONE_SIGMA/100, b=None):
        if b is None:
            left = (1 - a) / 2
            right = (1 + a) / 2
        else:
            left = a
            right = b

        return pd.Series(dict(left=self.bs().quantile(left),
                              right=self.bs().quantile(right),
                              value=self.nominal_value))

    def strip(self):
        return Variable(self.nominal_value, self.std_dev)

    def compare_lt(self, rhs):
        return (self.bs() < rhs.bs()).mean()

    def compare_le(self, rhs):
        return (self.bs() <= rhs.bs()).mean()

    def compare_gt(self, rhs):
        return (self.bs() > rhs.bs()).mean()

    def compare_ge(self, rhs):
        return (self.bs() >= rhs.bs()).mean()

    def prob(self, value):
        return self.compare_gt(value)

    def visualize(self):
        raise NotImplementedError