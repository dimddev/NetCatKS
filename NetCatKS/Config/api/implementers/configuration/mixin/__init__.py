"""
This module is written in a DynamicProtocol style and caring for our Mixin configuration
"""
from __future__ import absolute_import

from zope.interface import Interface, Attribute, implementer
from zope.component import getGlobalSiteManager

from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions


__author__ = 'dimd'


class MixinSharedConfig(BaseProtocolActions):
    """
    Represents a shared mixin configuration between all sections
    """
    def __init__(self):

        """
        We providing a default service name, port and hostname

        :return: void
        """
        self.__service_name = 'DefaultServiceName'
        self.__port = 8080
        self.__hostname = '127.0.0.1'

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
    def port(self):

        """
        Getter for a Service port
        :return: int
        """

        return self.__port

    @port.setter
    def port(self, port):

        """
        A Service port setter we accept only integers for a port number

        :param port:
        :type port: int

        :return: void

        """

        self.__port = port

    @property
    def hostname(self):
        """
        A WS hostname getter
        :return:
        """
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):

        """
        A WS hostname setter

        :param hostname:
        :type hostname: str

        :return: void
        """
        self.__hostname = hostname


class RegisterAsFactory(object):

    """
    A class that providing a shortcut for a register a class as Zope Factory
    This mechanism is a important for us because we having loaded all user defined callbacks and protocols
    on runtime, this including our internal configuration too
    """

    def __init__(self, klass):

        """

        The constructor will care about the class that have to be register as Factory
        :param klass:
        :type klass: class

        :return: void
        """

        self.__gsm = getGlobalSiteManager()
        self.__klass = klass

    def register(self):

        """
        Registering a class as Zope Factory, you can load this factory with a createObject

        :return: void
        """

        self.__gsm.registerUtility(
            Factory(self.__klass, self.__klass.__name__),
            IFactory,
            self.__klass.__name__.lower()
        )
