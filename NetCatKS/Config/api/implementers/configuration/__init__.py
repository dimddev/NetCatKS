"""
A container for all configuration API's
"""

from NetCatKS.Config.api.implementers.configuration.tcp import TCP
from NetCatKS.Config.api.implementers.configuration.web import WEB
from NetCatKS.Config.api.implementers.configuration.wamp import WAMP
from NetCatKS.Config.api.implementers.configuration.ws import WS

__author__ = 'dimd'

__all__ = [
    'TCP', 'WEB', 'WAMP', 'WS'
]
