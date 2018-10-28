from pandas import *

from functools import partialmethod

from uncertain_panda.bootstrapping.calculation import calculate_with_uncertainty, UncertaintyMode, \
    calculate_with_asymmetric_uncertainty
from uncertain_panda.bootstrapping.functions import LambdaFunction, NonNanNumpyFunction
from uncertain_panda.plotting.helpers import plot_with_uncertainty
from uncertain_panda.utils.numerics import coverage, pandas_coverage
from uncertain_panda.utils.pandas_utils import band, value_counts_with_uncertainty, groupbycut


def _get_uncertainty_calculation(f, mode):
    return partialmethod(calculate_with_uncertainty, f=f, mode=mode)


def _get_packed_function(attr, unstack=False):
    if unstack:
        return lambda x, *args, **kwargs: x.apply(lambda y: getattr(y, attr)(*args, **kwargs)).unstack()
    else:
        return lambda x, *args, **kwargs: x.apply(lambda y: getattr(y, attr)(*args, **kwargs))


def _add_basic_methods(core_object):
    core_object.coverage = pandas_coverage

    core_object.nominal_value = property(lambda x: x.apply(lambda y: y.nominal_value))
    core_object.std_dev = property(lambda x: x.apply(lambda y: y.std_dev))

    core_object.calculate_with_uncertainty = calculate_with_uncertainty
    core_object.calculate_with_asymmetric_uncertainty = calculate_with_asymmetric_uncertainty

    core_object.mean_with_uncertainty = _get_uncertainty_calculation(NonNanNumpyFunction("mean"),
                                                                     UncertaintyMode.bootstrapping)
    core_object.std_with_uncertainty = _get_uncertainty_calculation(NonNanNumpyFunction("std"),
                                                                    UncertaintyMode.bootstrapping)
    core_object.efficiency_with_uncertainty = _get_uncertainty_calculation(None, UncertaintyMode.binomial)
    # FIXME: this is quite slow!
    core_object.coverage_with_uncertainty = _get_uncertainty_calculation(LambdaFunction("coverage", coverage),
                                                                         UncertaintyMode.bootstrapping)
    core_object.value_counts_with_uncertainty = value_counts_with_uncertainty

    core_object.plot_with_uncertainty = plot_with_uncertainty
    core_object.band = band
    core_object.groupbycut = groupbycut


def _add_grouped_methods(core_object):
    class A: pass
    variables_before = set(vars(A))
    _add_basic_methods(A)
    variables_after = set(vars(A))

    functions_to_add = variables_after - variables_before

    for function_name in functions_to_add:
        setattr(core_object, function_name, _get_packed_function(function_name))

    core_object.band = _get_packed_function("band", unstack=True)


_add_basic_methods(Series)
_add_basic_methods(DataFrame)
_add_grouped_methods(core.groupby.SeriesGroupBy)
_add_grouped_methods(core.groupby.DataFrameGroupBy)