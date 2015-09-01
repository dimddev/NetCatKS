__author__ = 'dimd'

from zope.interface import Interface


class IRegisterFactory(Interface):

    def register_factories(**kwargs):
        """
        register factory into zope GSM
        :param kwargs:
        :return:
        """
