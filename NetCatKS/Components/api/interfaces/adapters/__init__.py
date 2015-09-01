__author__ = 'dimd'

from zope.interface import Interface


class IDynamicAdapterFactory(Interface):

    def get():
        """
        return new dynamic adapter prepared by __init__
        :return: class
        """
