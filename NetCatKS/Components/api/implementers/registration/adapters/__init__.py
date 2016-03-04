"""
A module that will load and register all API's registered under the follow
interfaces 'BaseAPI', 'BaseRootAPI', 'BaseRootAPIWampMixin', 'BaseAPIWampMixin', 'WAMPLoadOnRunTime'
Note: all of them have to be hosted inside an adapters directory otherwise will not be loaded!
"""

from datetime import datetime

from zope.component import getGlobalSiteManager, createObject
from zope.interface import implementer

from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.implementers.registration.factories import RegisterFactories
from NetCatKS.Components.api.interfaces import IJSONResourceAPI, IJSONResourceRootAPI, IWAMPLoadOnRunTime

from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.common.factory import RegisterAsFactory

__author__ = 'dimd'


@implementer(IRegisterAdapters)
class RegisterAdapters(RegisterFactories):

    """
    This class provide functionality for registering adapters inside Zope Global Site Manager
     ( storage of kind )
    """

    def __init__(self, protocols_source, file_loader=None, out_filter=None):

        """

        The constructor will initialize the storage, will load the loaded object
        that belong to our filters eg 'BaseAPI', 'BaseRootAPI', 'BaseRootAPIWampMixin',
        'BaseAPIWampMixin' and 'WAMPLoadOnRunTime'

        :param protocols_source:
        :param file_loader:
        :param out_filter:

        :return: void
        """

        # NETODO the arguments have to be clarify and described

        if not out_filter:
            out_filter = []

        default_filters = list(
            set(out_filter + [IVirtualAdapter, IJSONResourceAPI, IJSONResourceRootAPI, IWAMPLoadOnRunTime])
        )

        super(RegisterAdapters, self).__init__(protocols_source, file_loader, default_filters)

        self.__storage = createObject('storageregister')

        self.__objects = self.get_object()

        self.__gsm = getGlobalSiteManager()

    def register(self):

        """
        Will register all matched API's as subscriber adapters that will be called if they matched
        until our recognition process

        :return: True
        """

        # NETODO - the method always returning True - this is not correct

        if not isinstance(self.__objects, tuple) and not isinstance(self.__objects, list):
            raise TypeError('objects have to be tuple or list')

        self.__objects = list(set(self.__objects))

        __skip_system_helpers = [
            'BaseAPI', 'BaseRootAPI', 'BaseRootAPIWampMixin', 'BaseAPIWampMixin', 'WAMPLoadOnRunTime'
        ]

        for adapter, adapter_interface in self.__objects:

            if adapter.__name__ in __skip_system_helpers:
                continue

            print('{} [ RegisterAdapters ] Load: {} with filter: {}'.format(
                str(datetime.now()), adapter.__name__,
                adapter_interface.__name__
            ))

            self.__gsm.registerSubscriptionAdapter(adapter)

        return True


class FileAdaptersLoader(BaseLoader):

    """
    A helper class that is used until our loading process
    """

    def __init__(self, **kwargs):
        """
        Load all classes
        :param kwargs:
        :return:
        """
        super(FileAdaptersLoader, self).__init__(**kwargs)

RegisterAsFactory(RegisterAdapters).register()
