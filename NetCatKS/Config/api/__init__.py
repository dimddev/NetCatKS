"""
An API container
"""
from NetCatKS.Config.api.implementers.configuration.tcp import TCP
from NetCatKS.Config.api.implementers.configuration.ws import WS
from NetCatKS.Config.api.implementers.configuration.wamp import WAMP
from NetCatKS.Config.api.implementers.configuration.web import WEB
from NetCatKS.Config.api.implementers import Config

__author__ = 'dimd'

__all__ = [
    'Config',
    'TCP',
    'WEB',
    'WAMP',
    'WS'
]
