"""
A module contains a our main Interface that describe NetCatKS
"""
from zope.interface import Interface
__author__ = 'dimd'


class IDispatcher(Interface):
    """
    Main Dispatcher Interface
    """
    def dispatch(self):
        """
        Dispatch current message to actual factory
        :return:
        """


class IDispathcherResultHelper(Interface):
    """
    A helper interface for our result
    """
    def result_validation(self, sender, drop):
        """
        More info TBA
        :param sender:
        :param drop:
        :return:
        """

