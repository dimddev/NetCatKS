"""
This module is written in a DynamicProtocol style and caring for our WEB Socket Server configuration
"""
from __future__ import absolute_import

from zope.interface import Interface, Attribute, implementer
from NetCatKS.Config.api.implementers.configuration.mixin import RegisterAsFactory
from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.implementers.configuration.mixin import MixinSharedConfig

__author__ = 'dimd'


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
        self.__crt = 'keys/server.crt'

        self.__key = 'keys/server.key'

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


class WSImplementer(MixinSharedConfig):

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

        self.port = 8585

        self.service_name = 'Default Web Socket server'

        self.__keys = KeysImplementer()

        self.__url = 'ws://localhost:8585'

        self.__protocol = 'ws'

    @property
    def keys(self):

        """
        A keys getter

        :return: KeysImplementer
        """

        return self.__keys

    @keys.setter
    def keys(self, keys):

        """
        A key setter
        :param keys:
        :type keys: KeysImplementer

        :return: void
        """

        self.__keys = keys

    @property
    def url(self):
        """
        A WS URL getter
        :return:
        """
        return self.__url

    @url.setter
    def url(self, url):

        """
        A WS URL Setter
        :param url:
        :type url: str

        :return: void
        """
        self.__url = url

    @property
    def protocol(self):
        """
        A WS protocol getter
        :return: str
        """
        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):

        """
        A WS protocol setter. Protocol can be "ws" or "wss"
        :param protocol:
        :type protocol: str

        :return: void
        """
        __available_protocols = ['ws', 'wss']

        if protocol in __available_protocols:
            self.__protocol = protocol


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
