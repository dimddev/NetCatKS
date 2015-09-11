__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.adapters import IDynamicAdapterFactory
from NetCatKS.Components.api.interfaces.loaders import IBaseLoader
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactories
from NetCatKS.Components.api.interfaces.registration.protocols import IRegisterProtocols
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPResource, IRegisterWamp, IWAMPComponent
from NetCatKS.Components.api.interfaces.storages import IStorageRegister
from NetCatKS.Components.api.interfaces.loaders import IUserFactory, IUserStorage, IUserWampComponent, IUserGlobalSubscriber

__all__ = [
    'IDynamicAdapterFactory',
    'IBaseLoader',
    'IRegisterAdapters',
    'IRegisterFactories',
    'IRegisterProtocols',
    'IStorageRegister',
    'IWAMPResource',
    'IRegisterWamp',
    'IWAMPComponent',
    'IUserFactory',
    'IUserStorage',
    'IUserWampComponent',
    'IUserGlobalSubscriber'
]