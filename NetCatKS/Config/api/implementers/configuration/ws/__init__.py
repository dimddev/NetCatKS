"""
This module is written in a DynamicProtocol style and caring for our WEB Socket Server configuration
"""
from __future__ import absolute_import

from NetCatKS.Components.common.factory import RegisterAsFactory
from NetCatKS.Config.api.implementers.configuration.mixin import MixinSharedServiceName, MixinWamp, KeysImplementer

__author__ = 'dimd'


class WSImplementer(MixinWamp):

    """
    Implementation of IWSInterface
    """

    def __init__(self):

        """
        In our constructor we providing a default values for all properties
        :param kwargs:

        :return: void
        """

        super(WSImplementer, self).__init__()

        self.__service = MixinSharedServiceName()
        self.service = 'DefaultWSService'
        self.__ssl = KeysImplementer()

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, service_name):
        self.__service.name = service_name

    @property
    def ssl(self):
        return self.__ssl

    @ssl.setter
    def ssl(self, ssl):
        self.__ssl = ssl


class WS(WSImplementer):

    """
    A Proxy class, that represent a WSImplementer, use this
    """

    def __init__(self, **kwargs):
        """
        A constructor just call a super
        :param kwargs:
        :return:
        """
        super(WS, self).__init__(**kwargs)

RegisterAsFactory(WS).register()
