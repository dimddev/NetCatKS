__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.adapters import IDynamicAdapterFactory
from NetCatKS.Components.api.interfaces.loaders import IBaseLoader
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactory
from NetCatKS.Components.api.interfaces.registration.protocols import IProtocolRegister
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPResource, IWAMPRegister, IWAMPComponent
from NetCatKS.Components.api.interfaces.storages import IStorageRegister
from NetCatKS.Components.api.interfaces.loaders import IUserFactory, IUserStorage, IUserWampComponent, IUserGlobalSubscriber

__all__ = [
    'IDynamicAdapterFactory',
    'IBaseLoader',
    'IRegisterAdapters',
    'IRegisterFactory',
    'IProtocolRegister',
    'IStorageRegister',
    'IWAMPResource',
    'IWAMPRegister',
    'IWAMPComponent',
    'IUserFactory',
    'IUserStorage',
    'IUserWampComponent',
    'IUserGlobalSubscriber'
]