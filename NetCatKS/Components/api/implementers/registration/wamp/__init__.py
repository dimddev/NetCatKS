__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPRegister, IWAMPResource
from NetCatKS.Components.common.loaders import BaseLoader

from zope.interface import implementer
from zope.component import getGlobalSiteManager
# from zope.component import createObject


@implementer(IWAMPRegister)
class WampRegister(object):

    def __init__(self, file_loader, wamp_source):

        self.__gsm = getGlobalSiteManager()
        self.file_loader = file_loader

        self.__objects = self.file_loader.load(wamp_source)
        # self.__storage = createObject('storageregister')

        super(WampRegister, self).__init__()

    def register_wamp(self):

        if type(self.__objects) is not tuple and type(self.__objects) is not list:
            raise TypeError('objects have to be tuple or list')

        for obj in self.__objects:

            if obj.__name__.endswith('Wamp') and not obj.__name__.startswith('I'):

                self.__gsm.registerSubscriptionAdapter(obj)


class FileWampLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Adapter"
        :param kwargs:
        :return:
        """
        super(FileWampLoader, self).__init__(**kwargs)