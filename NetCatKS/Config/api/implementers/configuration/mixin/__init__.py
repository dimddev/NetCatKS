"""
This module is written in a DynamicProtocol style and caring for our Mixin configuration
"""
from __future__ import absolute_import
from zope.interface import Interface, Attribute, implementer
from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions


__author__ = 'dimd'


class MixinSharedServiceName(BaseProtocolActions):

    def __init__(self, **kwargs):
        """
        We providing a default service name

        :return: void
        """

        super(MixinSharedServiceName, self).__init__(**kwargs)

        self.__name = 'DefaultServiceName'

    @property
    def name(self):

        """
        A Service Name getter for this TCP service, it used inside out Twisted TCP service.Service

        :return: strs

        """

        return self.__name

    @name.setter
    def name(self, name):

        """
        A setter for a service name
        :param name:
        :type name: str

        :return: void
        """

        self.__name = name


class MixinSharedConfig(BaseProtocolActions):
    """
    Represents a shared mixin configuration between all sections
    """
    def __init__(self, **kwargs):

        """
        We providing a default service name, port and hostname

        :return: void
        """

        super(MixinSharedConfig, self).__init__(**kwargs)

        self.__service = MixinSharedServiceName()
        self.__port = 8080
        self.__hostname = '127.0.0.1'

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

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, service_name):
        self.__service.name = service_name


class MixinWamp(BaseProtocolActions):

    """
    A shared mixin for a web socket servers and wamp components
    """

    def __init__(self, **kwargs):

        """

        Our mixin providing a default values for a url - "ws://localhost:8585"
        and a protocol - "ws"

        :param kwargs:

        :return: void

        """
        super(MixinWamp, self).__init__(**kwargs)

        self.__url = 'ws://localhost:8585'

    @property
    def url(self):

        """
        A getter for our WS url
        :return: str
        """

        return self.__url

    @url.setter
    def url(self, url):

        """
        A setter for our WS url
        :param url:
        :type url: str

        :return: void
        """
        self.__url = url


class IKeysInterface(Interface):
    """
    Interface representing SSL keys. This keys are used when we creating a Secure WEB Socket server
    or knowing as WSS. This Interface is a child of our actual object
    """
    crt = Attribute("A SSL CRT key")

    key = Attribute("A SSL Private key")


@implementer(IKeysInterface)
class KeysImplementer(BaseProtocolActions):

    """
    Implementation of IKeysInterface
    """

    def __init__(self, **kwargs):
        """
        We providing a default place for our keys - inside a key directory
        eg on the same level where is located a app.py - project_root/keys/

        :param kwargs:

        :return: void
        """
        self.__crt = 'keys/serverpem.crt'

        self.__key = 'keys/serverpem.key'

    @property
    def crt(self):
        """
        A getter for a CRT key
        :return: str
        """
        return self.__crt

    @crt.setter
    def crt(self, crt):

        """
        A setter for a CRT key
        :param crt:
        :type crt: str

        :return: void

        """

        self.__crt = crt

    @property
    def key(self):
        """
        A getter for a prive key
        :return: str
        """
        return self.__key

    @key.setter
    def key(self, key):

        """
        A setter for a private key
        :param key:
        :type key: str

        :return: void
        """
        self.__key = key
