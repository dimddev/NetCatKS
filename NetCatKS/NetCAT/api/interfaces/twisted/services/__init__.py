"""
A module interface for a Twisted default TCP Service
"""

from zope.interface import Interface
from NetCatKS.NetCAT.api.interfaces.twisted.services.web import IDefaultWebService

__author__ = 'dimd'


class IDefaultService(Interface):
    """
    An interface for Twisted default TCP Service
    """
    def start():
        """
        Start default service
        :return:
        """

__all__ = [
    'IDefaultService',
    'IDefaultWebService'
]
