"""Pandas with uncertainties"""
__version__ = "0.2.0"

from .utils.pandas_utils import add_uncertainty_accessors
add_uncertainty_accessors()

from .uncertainties.calculation import UncertaintyMode

import pandas