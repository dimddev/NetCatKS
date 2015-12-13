"""
A container for all public object and interfaces related to our Component API
"""

from NetCatKS.Components.api import *
from NetCatKS.Components.common import *

__author__ = 'dimd'

__all__ = [
    'ComponentsRegistration',
    'DynamicAdapterFactory',
    'DefaultAdapter',
    'RegisterFactories',
    'RegisterAdapters',
    'RegisterProtocols',
    'StorageRegister',
    'IDynamicAdapterFactory',
    'IBaseLoader',
    'IRegisterAdapters',
    'IRegisterFactories',
    'IStorageRegister',
    'AdapterProxyGetter',
    'BaseLoader',
    'IRegisterWamp',
    'RegisterWamp',
    'IWAMPResource',
    'IJSONResourceRootAPI',
    'IJSONResourceAPI',
    'IJSONResource'
]
