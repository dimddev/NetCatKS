__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IDefaultFactory(Interface):
    """

    """
    config = Attribute('config as dict')
    protocol = Attribute('Factory used protocol')
    name = Attribute('Name of this service')
    port = Attribute('Port number')

__all__ = [
    'IDefaultFactory'
]
