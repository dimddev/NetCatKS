"""
This module is written in a DynamicProtocol style and caring for our WEB Server configuration
"""

from zope.interface import implementer

from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.interfaces import IWeb
from NetCatKS.Config.api.implementers.configuration.mixin import RegisterAsFactory

__author__ = 'dimd'


@implementer(IWeb)
class WEB(BaseProtocolActions):

    """
    A Class representing our base WEB configuration
    we having a simple setter and getters
    """

    def __init__(self):

        """

        In our constructor we having a default values for each
        property. Note: the default web method is "GET"

        :return: void
        """

        self.__service_name = 'Default WEB Server'
        self.__http_methods = ['GET']
        self.__port = 8000
        self.__www_root = ''

    @property
    def service_name(self):

        """
        Will return our web service name

        :return: str
        """

        return self.__service_name

    @service_name.setter
    def service_name(self, sname):

        """
        A setter for our WEB service name
        :param sname:
        :type sname: str

        :return: void
        """
        self.__service_name = sname

    @property
    def http_methods(self):

        """
        A getter for available http methods, by default there are only a "GET"
        if you need more methods, you have to edin your config file

        :return: list
        """
        return self.__http_methods

    @http_methods.setter
    def http_methods(self, methods):

        """
        A setter for an allowed http methods

        :param methods:
        :type methods: list

        :return: void
        """

        self.__http_methods = methods

    @property
    def port(self):

        """
        A WEB port gettger

        :return: int

        """
        return self.__port

    @port.setter
    def port(self, port):

        """

        :param port:
        :type port: int

        :return: void
        """
        self.__port = port

    @property
    def www_root(self):

        """
        A web root getter

        :return: str

        """

        return self.__www_root

    @www_root.setter
    def www_root(self, root):

        """
        A web root setter

        :param root:
        :type root: str

        :return: void
        """
        self.__www_root = root

RegisterAsFactory(WEB).register()
