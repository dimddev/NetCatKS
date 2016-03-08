"""
A interface that represent our Transfer Dynamic Object
"""

from zope.interface import Interface

__author__ = 'dimd'


class IDynamicTDO(Interface):

    """
    A interface that represent our Transfer Dynamic Object
    """

    def to_tdo(in_data):

        """
        Returning the computed TDO

        :param in_data:
        :type in_data: dict

        :return: dict
        """
