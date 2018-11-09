"""Pandas with uncertainties"""
__version__ = "0.1.0"

from .utils.pandas_utils import add_uncertainty_accessors
add_uncertainty_accessors()

from pandas import *