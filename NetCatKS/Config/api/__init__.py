"""
An API container
"""
from NetCatKS.Config.api.implementers.configuration import TCP, WS, WAMP, WEB
from NetCatKS.Config.api.implementers import Config

__author__ = 'dimd'

__all__ = [
    'Config',
    'TCP',
    'WEB',
    'WAMP',
    'WS'
]
