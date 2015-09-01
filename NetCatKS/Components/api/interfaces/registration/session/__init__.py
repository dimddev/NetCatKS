__author__ = 'dimd'

from zope.interface import Interface


class ISessionRegister(Interface):

    def register_sessions(**kwargs):
        """
        Register Sessions inside zope GSM
        :param kwargs:
        :return:
        """
