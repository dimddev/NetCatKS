"""
A module container
"""

from NetCatKS.NetCAT.api.interfaces.twisted.protocols.linereceiver import *
from NetCatKS.NetCAT.api.interfaces.twisted.factories import *
from NetCatKS.NetCAT.api.interfaces.twisted.services import *
from NetCatKS.NetCAT.api.interfaces.twisted.services.web import IDefaultWebService
from NetCatKS.NetCAT.api.interfaces.twisted.recources import IDefaultWebResource

__author__ = 'dimd'

__all__ = [
    'IDefaultFactory',
    'IDefaultLineReceiver',
    'IDefaultService',
    'IDefaultWebResource',
    'IDefaultWebService',
]
