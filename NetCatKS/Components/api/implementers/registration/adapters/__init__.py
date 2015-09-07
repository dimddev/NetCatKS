__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.implementers.adapters import DynamicAdapterFactory

from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.common.factory import get_factory_objects

from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
from zope.component import getGlobalSiteManager, createObject
from zope.interface import implementer


@implementer(IRegisterAdapters)
class RegisterAdapter(object):
    """
    This class provide functionality for registering adapters inside Zope Global Site Manager
     ( storage of kind )
    """
    def __init__(self, file_loader, adapters_source, **kwargs):

        super(RegisterAdapter, self).__init__()

        self.prefix = kwargs.get('factory_prefix', 'Adapter')
        # self.prefix = 'Factory'

        self.gsm = getGlobalSiteManager()
        self.__adapters = file_loader.load(adapters_source)
        self.__storage = createObject('storageregister')

    def register_adapters(self):
        """
        Registering of all adapters inside zope GSM each of them
        have to be provided by IVirtualAdapter
        :param adapters:
        :return: True on success or raise Exception
        """
        if type(self.__adapters) is not tuple and type(self.__adapters) is not list:
            raise TypeError('objects have to be tuple or list')

        for adapter in self.__adapters:

            if adapter.__name__.startswith('I'):
                continue

            print 'register adapter: {}'.format(adapter)
            self.gsm.registerAdapter(adapter)

        return True

    def get_multi_adapter(self, objects, belong_interface=IVirtualAdapter):
        """
        This function will return proper multi adapter
        :param objects: list of objects like ['user', 'admin']
        :param belong_interface: default is IVirtualAdapter
        :return: adapted object
        """

        # first we trying to get multi adapters based on all registered factories
        try:

            if type(objects) is not tuple and type(objects) is not list:
                raise TypeError('objects have to be tuple or list')

            return getMultiAdapter(get_factory_objects(objects), belong_interface)

        except ComponentLookupError:

                iface_collection = []

                for obj in objects:

                    iface_name = 'i{}{}'.format(obj, self.__storage.components.get(obj))
                    iface = self.__storage.interfaces.get(iface_name, None)

                    if iface:
                        iface_collection.append(iface.get('interface'))

                # will trying to make dynamic adapter based on current request

                DynamicAdapterFactory(iface_collection)
                return getMultiAdapter(get_factory_objects(objects), belong_interface)


class FileAdaptersLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Adapter"
        :param kwargs:
        :return:
        """
        super(FileAdaptersLoader, self).__init__(**kwargs)