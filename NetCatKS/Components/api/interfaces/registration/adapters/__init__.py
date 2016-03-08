"""
A module containing an interface for registration of adapters
"""

from zope.interface import Interface
__author__ = 'dimd'


class IRegisterAdapters(Interface):

    """
    Base interface for a RegisterAdapters implementation
    """

    def register_adapters(**kwargs):
        """
        register adapters into zope GSM
        :param kwargs:
        :return:
        """
