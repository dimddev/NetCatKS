from __future__ import absolute_import

__author__ = 'dimd'

from zope.interface import Interface, Attribute, implementer
from zope.component import getGlobalSiteManager

from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.DProtocol import BaseProtocolActions
from NetCatKS.Dispatcher import IJSONResource


class IKeysInterface(Interface):

    crt = Attribute("Comments going here")

    csr = Attribute("Comments going here")

    key = Attribute("Comments going here")

    pem = Attribute("Comments going here")

    pub = Attribute("Comments going here")


@implementer(IKeysInterface)
class KeysImplementer(BaseProtocolActions):

    def __init__(self, **kwargs):

        self.__crt = None

        self.__csr = None

        self.__key = None

        self.__pem = None

        self.__pub = None

    @property
    def crt(self):
        return self.__crt

    @crt.setter
    def crt(self, crt):
        self.__crt = crt

    @property
    def csr(self):
        return self.__csr

    @csr.setter
    def csr(self, csr):
        self.__csr = csr

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def pem(self):
        return self.__pem

    @pem.setter
    def pem(self, pem):
        self.__pem = pem

    @property
    def pub(self):
        return self.__pub

    @pub.setter
    def pub(self, pub):
        self.__pub = pub


class IWSInterface(Interface):

    keys = Attribute("Comments going here")

    url = Attribute("Comments going here")

    hostname = Attribute("Comments going here")

    port = Attribute("Comments going here")

    protocol = Attribute("Comments going here")


@implementer(IWSInterface)
class WSImplementer(BaseProtocolActions):

    def __init__(self, **kwargs):

        self.__keys = KeysImplementer()

        self.__url = 'ws://localhost:8585'

        self.__hostname = 'localhost'

        self.__port = 8585

        self.__protocol = 'ws'

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, keys):
        self.__keys = keys

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):
        self.__hostname = hostname

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):
        self.__protocol = protocol


@implementer(IJSONResource)
class WS(WSImplementer):

    def __init__(self, **kwargs):

        super(WS, self).__init__(**kwargs)


gsm = getGlobalSiteManager()

factory = Factory(WS, WS.__name__)
gsm.registerUtility(factory, IFactory, WS.__name__.lower())

