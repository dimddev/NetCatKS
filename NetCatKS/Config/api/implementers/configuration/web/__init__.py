"""
This module is written in a DynamicProtocol style and caring for our WEB Server configuration
"""

from zope.interface import implementer

from NetCatKS.Config.api.interfaces import IWeb

from NetCatKS.Config.api.implementers.configuration.mixin import MixinSharedConfig
from NetCatKS.Components.common.factory import RegisterAsFactory

__author__ = 'dimd'


@implementer(IWeb)
class WEB(MixinSharedConfig):

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
        super(WEB, self).__init__()
        self.service = 'DefaultWEBService'
        self.__http_methods = ['GET']
        self.__www_root = ''

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
