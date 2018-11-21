import pandas as pd

from uncertain_panda.uncertainties.calculation import create_uncertainty, UncertaintyMode
from uncertain_panda.uncertainties.functions import LambdaFunction, NonNanNumpyFunction, PandasFunction
from uncertain_panda.plotting.helpers import plot_with_uncertainty
from uncertain_panda.utils.numerics import coverage, pandas_coverage, value_counts


import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from uncertainties import nominal_value, std_dev

ONE_SIGMA = 68.2689


class UncertaintyDirectAccessor(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

        self._add_shortcut_function("mean", NonNanNumpyFunction("mean"))
        self._add_shortcut_function("std", NonNanNumpyFunction("std"))
        self._add_shortcut_function("coverage", LambdaFunction("coverage", coverage))
        self._add_shortcut_function("efficiency", NonNanNumpyFunction("mean"), mode=UncertaintyMode.binomial)

    # Special function
    def value_counts(self, *args, normalize=False, **kwargs):
        return value_counts(df=self._obj, *args, normalize=normalize, **kwargs)

    # General accessor
    def __getattr__(self, function_name):
        return self._add_shortcut_function(function_name, PandasFunction(function_name))

    def _add_shortcut_function(self, function_name, function_object, mode=UncertaintyMode.bootstrapping):
        def wrapped_function(*args, **kwargs):
            return create_uncertainty(self._obj, *args, f=function_object, mode=mode, **kwargs)

        setattr(self, function_name, wrapped_function)
        return wrapped_function


def add_correct_stuff(df):
    df.bs = lambda: applied_bs(df)
    df.ci = lambda *args, **kwargs: applied_ci(df, *args, **kwargs)


class UncertaintyAggregateAccessor(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __getattr__(self, item):
        def wrapped_function(*args, **kwargs):
            # TODO: it is computational clever to do the sampling on the full data frame!
            s = self._obj.aggregate(lambda x: getattr(x.unc, item)(*args, **kwargs))
            add_correct_stuff(s)
            return s

        setattr(self, item, wrapped_function)
        return wrapped_function


def applied_nominal_value(x):
    try:
        return x.apply(lambda y: applied_nominal_value(y))
    except AttributeError:
        return nominal_value(x)


def applied_std_dev(x):
    try:
        return x.apply(lambda y: applied_std_dev(y))
    except AttributeError:
        return std_dev(x)


def applied_bs(x):
    if isinstance(x, pd.Series):
        return x.apply(lambda y: applied_bs(y)).T

    if isinstance(x, pd.DataFrame):
        return pd.concat({column: applied_bs(series).T for column, series in x.iteritems()}).T

    return x.bs()


def applied_ci(x, *args, **kwargs):
    if isinstance(x, pd.Series):
        return x.apply(lambda y: applied_ci(y, *args, **kwargs))

    if isinstance(x, pd.DataFrame):
        return pd.concat({column: applied_ci(series, *args, **kwargs).T for column, series in x.iteritems()}).T

    return x.ci(*args, **kwargs)


def _add_basic_methods(core_object):
    core_object.coverage = pandas_coverage

    core_object.nominal_value = property(applied_nominal_value)
    core_object.std_dev = property(applied_std_dev)

    core_object.plot_with_uncertainty = plot_with_uncertainty


def add_uncertainty_accessors():
    _add_basic_methods(pd.Series)
    _add_basic_methods(pd.DataFrame)

    pd.core.accessor.register_series_accessor("unc")(UncertaintyDirectAccessor)

    pd.core.accessor.register_dataframe_accessor("unc")(UncertaintyAggregateAccessor)
    pd.core.groupby.SeriesGroupBy.unc = pd.core.accessor.CachedAccessor("unc", UncertaintyAggregateAccessor)
    pd.core.groupby.DataFrameGroupBy.unc = pd.core.accessor.CachedAccessor("unc", UncertaintyAggregateAccessor)
