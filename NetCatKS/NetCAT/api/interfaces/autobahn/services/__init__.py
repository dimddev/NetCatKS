"""
A module service interface
"""
from zope.interface import Interface

__author__ = 'dimd'


class IDefaultAutobahnService(Interface):

    """
    An interface represent a default WAMP service
    """

    def start():
        """
        Start default service
        :return:
        """


class IDefaultWSService(Interface):

    """
    An interface represent a default WS service
    """

    def start():
        """
        Start default service
        :return:
        """

__all__ = [
    'IDefaultAutobahnService',
    'IDefaultWSService'
]
