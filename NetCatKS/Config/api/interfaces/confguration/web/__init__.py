"""
A module contain an interface representing a web part of a config
"""

from zope.interface import Interface, Attribute
__author__ = 'dimd'


class IWeb(Interface):

    """
    An interface describing a web part of a config
    """

    service_name = Attribute('A name of this web service')
    http_methods = Attribute('A List of methods')
    port = Attribute('Port number')
    www_root = Attribute('Web (www) root')
