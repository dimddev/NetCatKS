"""
A container for configuration interfaces
"""
from NetCatKS.Config.api.interfaces.confguration.tcp import ITcp
from NetCatKS.Config.api.interfaces.confguration.web import IWeb
from NetCatKS.Config.api.interfaces.confguration.wamp import IWamp, IWampCra

__author__ = 'dimd'

__all__ = [
    'ITcp',
    'IWeb',
    'IWamp',
    'IWampCra'
]
