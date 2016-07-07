"""
This module is written in a DynamicProtocol style and caring for our TCP Server configuration
"""

from __future__ import absolute_import

from zope.interface import implementer
from NetCatKS.Components.common.factory import RegisterAsFactory
from NetCatKS.Config.api.interfaces import ITcp
from NetCatKS.Config.api.implementers.configuration.mixin import MixinSharedConfig

__author__ = 'dimd'


@implementer(ITcp)
class TCP(MixinSharedConfig):

    """

    A Class representing our base TCP configuration
    we having a simple setter and getters

    """
    def __init__(self):

        """
        In the constructor we having a default settings for our config,
        all generated configs will having this settings
        :return: void

        """

        super(TCP, self).__init__()

        self.port = 8484
        self.service = 'Default TCP Server'

        self.__tcp_back_log = 50
        self.__type = 'server'

    @property
    def tcp_back_log(self):

        """
        TCP back log getter

        :return: int

        """

        return self.__tcp_back_log

    @tcp_back_log.setter
    def tcp_back_log(self, back_log):

        """
        A TCP back log setter

        :param back_log:
        :type back_log: int

        :return: void
        """

        self.__tcp_back_log = back_log

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, t):
        self.__type = t

RegisterAsFactory(TCP).register()
