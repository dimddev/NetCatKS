__author__ = 'dimd'

from zope.interface import Interface


class IProtocolRegister(Interface):

    def register_protocols(**kwargs):
        """
        Register Sessions inside zope GSM
        :param kwargs:
        :return:
        """
