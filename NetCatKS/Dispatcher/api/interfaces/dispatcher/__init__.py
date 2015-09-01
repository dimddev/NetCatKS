__author__ = 'dimd'

from zope.interface import Interface


class IDispatcher(Interface):

    def dispatch(self):
        """
        Dispatch current message to actual factory
        :return:
        """
