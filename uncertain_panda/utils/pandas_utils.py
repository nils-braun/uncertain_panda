import pandas as pd
from uncertainties import nominal_value, std_dev

from uncertain_panda.uncertainties import calculate_with_asymmetric_uncertainty
from uncertain_panda.uncertainties.calculation import calculate_with_uncertainty, UncertaintyMode
from uncertain_panda.uncertainties.functions import LambdaFunction, NonNanNumpyFunction, PandasFunction
from uncertain_panda.plotting.helpers import plot_with_uncertainty
from uncertain_panda.utils.numerics import coverage, pandas_coverage, value_counts


class UncertaintySeriesAccessor(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

        self._add_shortcut_function("mean", NonNanNumpyFunction("mean"))
        self._add_shortcut_function("std", NonNanNumpyFunction("std"))
        self._add_shortcut_function("coverage", LambdaFunction("coverage", coverage))

    def _add_shortcut_function(self, function_name, function_object):
        def wrapped_function(*args, **kwargs):
            return self.__class__.uncertainty_function(self._obj, *args, f=function_object,
                                                       mode=UncertaintyMode.bootstrapping,
                                                       **kwargs)

        setattr(self, function_name, wrapped_function)

    # Special functions
    def efficiency(self, *args, **kwargs):
        return self.__class__.uncertainty_function(self._obj, *args, f=None, mode=UncertaintyMode.binomial,
                                                   **kwargs)

    def value_counts(self, *args, normalize=False, **kwargs):
        return value_counts(df=self._obj, *args, normalize=normalize, **kwargs)

    # General accessor
    def __getattr__(self, item):
        def wrapped_function(*args, **kwargs):
            return self.__class__.uncertainty_function(self._obj, *args, f=PandasFunction(item),
                                                       mode=UncertaintyMode.bootstrapping, **kwargs)

        setattr(self, item, wrapped_function)
        return wrapped_function


class UncertaintyDataFrameAccessor(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __getattr__(self, item):
        def wrapped_function(*args, **kwargs):
            return self._obj.apply(lambda x: getattr(getattr(x, self.__class__.wrapped_name), item)(*args, **kwargs))

        setattr(self, item, wrapped_function)
        return wrapped_function


def _add_basic_methods(core_object):
    core_object.coverage = pandas_coverage

    core_object.nominal_value = property(lambda x: x.apply(lambda y: nominal_value(y)))
    core_object.std_dev = property(lambda x: x.apply(lambda y: std_dev(y)))

    core_object.plot_with_uncertainty = plot_with_uncertainty
    # core_object.band = band


def add_uncertainty_accessors():
    _add_basic_methods(pd.DataFrame)
    _add_basic_methods(pd.Series)

    @pd.core.accessor.register_series_accessor("unc")
    class SymmetricUncertaintySeriesAccessor(UncertaintySeriesAccessor):
        uncertainty_function = calculate_with_uncertainty

    @pd.core.accessor.register_series_accessor("unc_asym")
    class AsymmetricUncertaintySeriesAccessor(UncertaintySeriesAccessor):
        uncertainty_function = calculate_with_asymmetric_uncertainty

    @pd.core.accessor.register_dataframe_accessor("unc")
    class SymmetricUncertaintyDataFrameAccessor(UncertaintyDataFrameAccessor):
        wrapped_name = "unc"

    @pd.core.accessor.register_dataframe_accessor("unc_asym")
    class AsymmetricUncertaintyDataFrameAccessor(UncertaintyDataFrameAccessor):
        wrapped_name = "unc_asym"

    pd.core.groupby.DataFrameGroupBy.unc = pd.core.accessor.CachedAccessor("unc", SymmetricUncertaintyDataFrameAccessor)
    pd.core.groupby.DataFrameGroupBy.unc_asym = pd.core.accessor.CachedAccessor("unc_asym",
                                                                                AsymmetricUncertaintyDataFrameAccessor)
