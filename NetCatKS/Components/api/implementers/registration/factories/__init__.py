__author__ = 'dimd'

from datetime import datetime

from zope.interface import implementer
from zope.component import createObject
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactory
from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Logger import Logger


@implementer(IRegisterFactory)
class RegisterFactory(object):

    def __init__(self, file_loader, factories):
        """

        :param file_loader:
        :param factories:
        :return:
        """

        super(RegisterFactory, self).__init__()

        self.__gsm = getGlobalSiteManager()
        self.file_loader = file_loader
        self.__objects = self.file_loader.load(factories)

        self.__storage = createObject('storageregister')
        self.__logger = Logger()

    def register_factories(self):
        """

        :return:
        """
        if type(self.__objects) is not tuple and type(self.__objects) is not list:
            raise TypeError('objects have to be tuple or list')

        self.__objects = set(self.__objects)

        for obj in self.__objects:

            __ignore = ['Factory', 'IFactory']

            if obj.__name__ in __ignore:
                continue

            print('{} [RegisterFactory] Load factory : {}'.format(str(datetime.now()), obj.__name__))

            reg_name = obj.__name__.lower().replace(self.file_loader.prefix.lower(), '')
            self.__storage.components[reg_name] = self.file_loader.prefix.lower()

            factory = Factory(obj, obj.__name__)
            self.__gsm.registerUtility(factory, IFactory, obj.__name__.lower())


class FileFactoryLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Factory"
        :param kwargs:
        :return:
        """
        super(FileFactoryLoader, self).__init__(**kwargs)