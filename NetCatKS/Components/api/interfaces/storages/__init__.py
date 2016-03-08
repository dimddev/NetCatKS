"""
A module for our storage interface
"""

from zope.interface import Interface, Attribute
__author__ = 'dimd'


class IStorageRegister(Interface):
    """
    A base interface for our internal storage API
    """
    components = Attribute("keep registered components")
    interfaces = Attribute("keep registered interfaces")
