"""
Our public container from Dispatcher API
"""
from NetCatKS.Dispatcher.api.interfaces.dispatcher import IDispatcher, IDispathcherResultHelper
from NetCatKS.Dispatcher.api.implementers.dispatcher import Dispatcher
from NetCatKS.Dispatcher.api.implementers.dispatcher import DispathcherResultHelper

__author__ = 'dimd'

__all__ = [
    'IDispatcher',
    'Dispatcher',
    'DispathcherResultHelper',
    'IDispathcherResultHelper'
]
