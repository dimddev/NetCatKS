"""
A module containing an interface for registration of protocols
"""
from zope.interface import Interface

__author__ = 'dimd'


class IRegisterProtocols(Interface):

    """
    Base interface for a implementation of RegisterProtocols
    """

    def register(**kwargs):
        """
        Register Sessions inside zope GSM
        :param kwargs:
        :return:
        """
