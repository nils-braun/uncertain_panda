import pandas as pd

from ..utils.numerics import ONE_SIGMA

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from uncertainties.core import Variable


def _apply_bs(x):
    try:
        return x.bs()
    except AttributeError:
        return x


class BootstrapResult(Variable):
    """
    Result of any calculation performed with the `unc` wrapper.
    It is an instance of :class:`uncertainties.core.Variable`, so
    it behaves like a normal number with uncertainties.
    """
    def __init__(self, nominal_value, bootstrap):
        self._bootstrap = bootstrap

        super().__init__(nominal_value, self.bs().std())

    def bs(self):
        """
        Return the full data sample of bootstrapped results.
        Usually used for visualisations, such as::

            df["var"].unc.mean().bs().plot(kind="hist")
        """
        return self._bootstrap

    def ci(self, a=ONE_SIGMA / 100, b=None):
        """
        Return the confidence interval between ``a`` and ``b``.
        This is the pair of values [left, right], so that
        a fraction ``a`` of the bootstrapped results is left of ``left``
        and ``b`` of the results is right of ``right``.
        If you only give one parameter, the symmetric interval with ``b = a`` is returned.
        :return: a :class:`pd.Series` with the columns ``value``, ``left`` and ``right``.
        """
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
        """
        This result still includes the full sample of bootstrapped results.
        So it can be quite heavy (in terms of memory).
        The function returns an uncertainty number without the bootstrapped histogram.
        """
        return Variable(self.nominal_value, self.std_dev)

    def compare_lt(self, rhs):
        """How many of the values are < than ``rhs``?"""
        return (self.bs() < _apply_bs(rhs)).mean()

    def compare_le(self, rhs):
        """How many of the values are <= than ``rhs``?"""
        return (self.bs() <= _apply_bs(rhs)).mean()

    def compare_gt(self, rhs):
        """How many of the values are > than ``rhs``?"""
        return (self.bs() > _apply_bs(rhs)).mean()

    def compare_ge(self, rhs):
        """How many of the values are >= than ``rhs``?"""
        return (self.bs() >= _apply_bs(rhs)).mean()

    def prob(self, value):
        """
        Return the probability to have a resut equal or greater than ``value``.

        If we assume the bootstrapped results are a probability density function,
        this is equivalent to the p-value.
        """
        return self.compare_gt(value)