"""
A module contains an interface which represent a WAMP part of a config
"""

from zope.interface import Interface, Attribute
__author__ = 'dimd'


class IWamp(Interface):

    """
    Interface that describe a wamp part of config
    """

    user = Attribute('WAMP CRA User')
    password = Attribute('WAMP CRA password')
    realm = Attribute('WAMP Realm')
    retry_interval = Attribute('If connection is lost, we will trying to reconnect via this interrval')
    path = Attribute('Pato from wamp url')
