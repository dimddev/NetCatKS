"""
A module that contains functionality that will register API's from
IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent type as
subscription adapters and later when onJoin occur they will be loaded and
registered inside our wamp session as well
"""

from __future__ import absolute_import

from datetime import datetime

from zope.interface import implementer
from zope.component import getGlobalSiteManager

from NetCatKS.Components.api.interfaces.registration.wamp import IRegisterWamp
from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.common.factory import RegisterAsFactory
from NetCatKS.Components.api.interfaces import IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent

__author__ = 'dimd'


@implementer(IRegisterWamp)
class RegisterWamp(object):

    """
    Take care for registration of all wamp components
    """

    def __init__(self, wamp_source, file_loader=None, out_filter=None):
        """

        :param file_loader:
        :param wamp_source:
        :param out_filter:

        :return: void
        """

        self.__gsm = getGlobalSiteManager()
        self.file_loader = file_loader or FileWampLoader()

        self.default_filter = out_filter or [IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent]

        self.__objects = self.file_loader.load(
            wamp_source, self.default_filter

        )

        super(RegisterWamp, self).__init__()

    def register(self):

        """
        Will register API's from IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent type
        as subscription adapters

        :return: void
        """
        if not isinstance(self.__objects, tuple) and not isinstance(self.__objects, list):
            raise TypeError('objects have to be tuple or list')

        __ignore_list = [
            'BaseWampComponent'
        ]

        for obj, obj_interface in self.__objects:

            if obj.__name__ in __ignore_list:
                continue

            print('{} [ RegisterWamp ] Loading Wamp Component: id: {}, {}, filter interface: {}'.format(
                datetime.now(), id(obj), obj.__name__, obj_interface.__name__
            ))

            self.__gsm.registerSubscriptionAdapter(obj)
            # RegisterAsFactory(obj).register()


class FileWampLoader(BaseLoader):

    """
    A helper class that is used during our loading process
    """

    def __init__(self, **kwargs):

        """
        Just call a super
        :param kwargs:
        :return: void
        """
        super(FileWampLoader, self).__init__(**kwargs)

RegisterAsFactory(RegisterWamp).register()
