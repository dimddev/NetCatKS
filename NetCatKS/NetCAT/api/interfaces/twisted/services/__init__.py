__author__ = 'dimd'

from zope.interface import Interface


class IDefaultService(Interface):

    def start():
        """
        Start default service
        :return:
        """

__all__ = [
    'IDefaultService'
]

