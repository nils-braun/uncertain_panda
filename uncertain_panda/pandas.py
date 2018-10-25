from functools import partialmethod

from pandas import *

from uncertain_panda.bootstrapping.calculation import calculate_with_uncertainty, UncertaintyMode, \
    calculate_with_asymmetric_uncertainty
from uncertain_panda.bootstrapping.functions import NumpyFunction, LambdaFunction, NonNanNumpyFunction
from uncertain_panda.plotting.helpers import plot_with_uncertainty
from uncertain_panda.utils.numerics import coverage, pandas_coverage
from uncertain_panda.utils.pandas_utils import band, value_counts_with_uncertainty


def _add_uncertainty_calculation(f, mode):
    return partialmethod(calculate_with_uncertainty, f=f, mode=mode)


def _add_basic_methods(core_object):
    # def _packed(attr, unstack=False):
    #     if unstack:
    #         return lambda x, *args, **kwargs: x.apply(lambda y: getattr(y, attr)(*args, **kwargs)).unstack()
    #     else:
    #         return lambda x, *args, **kwargs: x.apply(lambda y: getattr(y, attr)(*args, **kwargs))
    #
    # if groupby:
    #     core_object.calculate_with_uncertainty = _packed(
    #         "calculate_with_uncertainty", unstack=False)
    #     core_object.mean_with_uncertainty = _packed(
    #         "mean_with_uncertainty", unstack=False)
    #     core_object.efficiency_with_uncertainty = _packed(
    #         "efficiency_with_uncertainty", unstack=False)
    #     core_object.std_with_uncertainty = _packed(
    #         "std_with_uncertainty", unstack=False)
    #     core_object.median_with_uncertainty = _packed(
    #         "median_with_uncertainty", unstack=False)
    #     core_object.coverage_with_uncertainty = _packed(
    #         "coverage_with_uncertainty", unstack=False)
    #     core_object.calculate_efficiency = _packed(
    #         "calculate_efficiency", unstack=False)
    #     core_object.coverage = _packed("coverage", unstack=False)
    #     core_object.band = _packed("band", unstack=True)
    #     core_object.value_counts_with_uncertainty = _packed("value_counts_with_uncertainty", unstack=False)
    #
    # else:
    core_object.coverage = pandas_coverage

    core_object.nominal_value = property(lambda x: x.apply(lambda y: y.nominal_value))
    core_object.std_dev = property(lambda x: x.apply(lambda y: y.std_dev))

    core_object.calculate_with_uncertainty = calculate_with_uncertainty
    core_object.calculate_with_asymmetric_uncertainty = calculate_with_asymmetric_uncertainty

    core_object.mean_with_uncertainty = _add_uncertainty_calculation(NonNanNumpyFunction("mean"), UncertaintyMode.bootstrapping)
    core_object.std_with_uncertainty = _add_uncertainty_calculation(NonNanNumpyFunction("std"), UncertaintyMode.bootstrapping)
    # TODO: currently there is no usable median/percentile50 function is dask, that applys to only one axis...
    # # core_object.median_with_uncertainty = _add_uncertainty_calculation(NonNanNumpyFunction("percentile", q=50), UncertaintyMode.bootstrapping)
    core_object.efficiency_with_uncertainty = _add_uncertainty_calculation(None, UncertaintyMode.binomial)
    # FIXME: this is quite slow!
    core_object.coverage_with_uncertainty = _add_uncertainty_calculation(LambdaFunction("coverage", coverage), UncertaintyMode.bootstrapping)
    core_object.value_counts_with_uncertainty = value_counts_with_uncertainty

    core_object.plot_with_uncertainty = plot_with_uncertainty
    core_object.band = band


_add_basic_methods(Series)
_add_basic_methods(DataFrame)
#_add_basic_methods(core.groupby.SeriesGroupBy, groupby=True)
#_add_basic_methods(core.groupby.DataFrameGroupBy, groupby=True)


# def groupbycut(df, variable, bins):
#     tmp = df.copy()
#     if isinstance(variable, str):
#         variable = df[variable]
#     tmp["bins"] = to_numeric(cut(variable, bins).apply(lambda x: x.mid))
#     return tmp.groupby("bins")
#
# DataFrame.groupbycut = groupbycut
