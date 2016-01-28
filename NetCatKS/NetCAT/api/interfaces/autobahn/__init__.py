"""
A module container
"""

from NetCatKS.NetCAT.api.interfaces.autobahn.components import IWampDefaultComponent
from NetCatKS.NetCAT.api.interfaces.autobahn.services import *
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultAutobahnFactory
from NetCatKS.NetCAT.api.interfaces.autobahn.protocols import IWSProtocol
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory

__author__ = 'dimd'

__all__ = [
    'IWampDefaultComponent',
    'IDefaultAutobahnService',
    'IDefaultAutobahnFactory',
    'IDefaultWSService',
    'IWSProtocol',
    'IDefaultWSFactory'
]
