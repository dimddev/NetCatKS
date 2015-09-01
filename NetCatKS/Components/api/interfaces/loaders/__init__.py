__author__ = 'dimd'

from zope.interface import Interface


class IBaseLoader(Interface):

    def load(self):
        """

        :return:
        """
