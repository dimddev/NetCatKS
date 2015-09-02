__author__ = 'dimd'

from zope.interface import Interface


class IConfig(Interface):

    def get():
        """
        Load from json and accsess as dict
        :return: dict
        """
