"""
A module that providing a base functionality for loading and registration of API's
"""
from __future__ import absolute_import

from datetime import datetime

from zope.interface import implementer
from zope.component import createObject
from zope.component import getGlobalSiteManager

from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactories
from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.api.interfaces import IUserStorage, IUserFactory
from NetCatKS.Validators import IValidatorResponse
from NetCatKS.DProtocol import DProtocolSubscriber
from NetCatKS.Logger import Logger
from NetCatKS.Components.api.interfaces import IJSONResource
from NetCatKS.Components.common.factory import RegisterAsFactory


__author__ = 'dimd'


@implementer(IRegisterFactories)
class RegisterFactories(object):

    """
    A class that care about all API's  registered with IUserStorage and IUserFactory interfaces
    plus user defined. This class is a base for all the others from a Register* family
    """

    def __init__(self, factories_source, file_loader=None, out_filter=None):

        """
        The constructor will init the storage and all objects that are matched from our filters

        :param file_loader:
        :param factories_source:

        :return: void
        """

        super(RegisterFactories, self).__init__()

        self.__gsm = getGlobalSiteManager()

        self.file_loader = file_loader or FileFactoryLoader()

        if not out_filter:
            out_filter = []

        self.default_filter = list(set(out_filter + [IUserStorage, IUserFactory]))

        self.__objects = self.file_loader.load(
            factories_source, self.default_filter

        )

        self.__storage = createObject('storageregister')
        self.__logger = Logger()

    def get_object(self):

        """
        A getter for all loaded objects

        :return: object
        """

        return self.__objects

    def register(self):
        """
        Will register API's
        :return: void
        """

        # NETODO the docs have to be improved

        if not isinstance(self.__objects, tuple) and not isinstance(self.__objects, list):
            raise TypeError('objects have to be tuple or list')

        self.__objects = set(self.__objects)

        for obj, obj_interface in self.__objects:

            __ignore = ['Factory', 'IFactory']

            if obj.__name__ in __ignore:
                continue

            print('{} [ RegisterFactories ] Load: {} with filter: {}'.format(
                str(datetime.now()), obj.__name__,
                obj_interface.__name__
            ))

            if obj_interface is IJSONResource:

                try:

                    subscribe_me = getattr(obj(), 'subscribe_me')()

                except AttributeError:
                    pass

                else:

                    def __init(self, adapter):
                        self.adapter = adapter

                    if subscribe_me is True:

                        __klass = type(
                            'DynamicAdapter{}'.format(obj.__name__),
                            (DProtocolSubscriber, ),
                            {'__init__': __init, 'protocol': None}
                        )

                        setattr(__klass, 'protocol', obj())
                        self.__gsm.registerSubscriptionAdapter(__klass, [IValidatorResponse])

            # NETODO to be checked and removed is needed

            RegisterAsFactory(obj).register()


class FileFactoryLoader(BaseLoader):

    """
    A helper class that is used during our loading process
    """

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Factory"
        :param kwargs:
        :return:
        """
        super(FileFactoryLoader, self).__init__(**kwargs)

RegisterAsFactory(RegisterFactories).register()
