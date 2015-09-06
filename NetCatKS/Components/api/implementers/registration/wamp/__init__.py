__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPRegister
from NetCatKS.Components.common.loaders import BaseLoader

from zope.interface import implementer
from zope.component import getGlobalSiteManager


@implementer(IWAMPRegister)
class WampRegister(object):

    """
    Take care for registration of all wamp components
    """

    def __init__(self, file_loader, wamp_source):
        """

        :param file_loader:
        :param wamp_source:
        :return:
        """

        self.__gsm = getGlobalSiteManager()
        self.file_loader = file_loader

        self.__objects = self.file_loader.load(wamp_source)

        super(WampRegister, self).__init__()

    def register_wamp(self):
        """

        :return:
        """
        if type(self.__objects) is not tuple and type(self.__objects) is not list:
            raise TypeError('objects have to be tuple or list')

        for obj in self.__objects:

            if obj.__name__.endswith(self.file_loader.prefix) and not obj.__name__.startswith('I'):

                self.__gsm.registerSubscriptionAdapter(obj)


class FileWampLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] eg. 'Wamp', default is 'Adapter"
        :param kwargs:
        :return:
        """
        super(FileWampLoader, self).__init__(**kwargs)