"""
A module containing an interface for registration of factories
"""
from zope.interface import Interface
__author__ = 'dimd'


class IRegisterFactories(Interface):

    """
    Base interface for a implementation of RegisterFactories
    """

    def register(**kwargs):
        """
        register factory into zope GSM
        :param kwargs:
        :return:
        """
