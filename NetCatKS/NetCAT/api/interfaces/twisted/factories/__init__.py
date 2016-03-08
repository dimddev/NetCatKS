"""
A module that providing a interface for a Twisted TCP and WEB Factories
"""
from zope.interface import Interface, Attribute

__author__ = 'dimd'


class IDefaultFactory(Interface):
    """
    A default twisted TCP factory config
    """
    config = Attribute('config as dict')
    protocol = Attribute('Factory used protocol')
    name = Attribute('Name of this service')
    port = Attribute('Port number')


class IDefaultWebFactory(Interface):
    """
    A default twisted WEB factory config
    """
    config = Attribute('config as dict')
    name = Attribute('Name of this service')
    port = Attribute('Port number')
    methods = Attribute('A list that contains all allowed methods: GET, POST... etc')


__all__ = [
    'IDefaultFactory',
    'IDefaultWebFactory'
]
