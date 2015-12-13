"""
This module is written in a DynamicProtocol style and caring for our TCP Server configuration
"""

from __future__ import absolute_import

from zope.interface import implementer

from NetCatKS.Config.api.implementers.configuration.mixin import RegisterAsFactory
from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.interfaces import ITcp

__author__ = 'dimd'


@implementer(ITcp)
class TCP(BaseProtocolActions):

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

        self.__port = 8484
        self.__service_name = 'Default TCP Server'
        self.__tcp_back_log = 50

    @property
    def port(self):

        """
        Getter for a TCP port
        :return: int
        """

        return self.__port

    @port.setter
    def port(self, port):

        """
        A port setter we accept only integers for a port number

        :param port:
        :type port: int

        :return: void

        """

        self.__port = port

    @property
    def service_name(self):

        """
        A Service Name getter for this TCP service, it used inside out Twisted TCP service.Service

        :return: strs

        """

        return self.__service_name

    @service_name.setter
    def service_name(self, name):

        """
        A setter for a service name
        :param name:
        :type name: str

        :return: void
        """

        self.__service_name = name

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


RegisterAsFactory(TCP).register()
