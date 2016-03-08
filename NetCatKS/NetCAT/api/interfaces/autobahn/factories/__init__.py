"""
A module that contains an interfaces for all default factories
"""
from zope.interface import Interface, Attribute

__author__ = 'dimd'


class IDefaultAutobahnFactory(Interface):

    """
    An interface for a DefaultAutobahnFactory implementation aka a WAMP component
    """

    protocol = Attribute('WAMP protocol can be ws or wss')
    name = Attribute('Service name')
    port = Attribute('WAMP port usually crossbar WS')
    host = Attribute('WAMP host')
    path = Attribute('WAMP path for example: ws://localhost/path')
    realm = Attribute('WAMP Realm')


class IDefaultWSFactory(Interface):

    """
    An interface for a DefaultWSFactory implementation
    """

    protocol = Attribute('WS protocol can be ws or wss')
    name = Attribute('Service name')
    port = Attribute('WS port usually crossbar WS')
    host = Attribute('WS host')
    path = Attribute('WS path for example: ws://localhost/path')
    realm = Attribute('WS Realm')

