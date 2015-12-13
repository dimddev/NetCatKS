"""
A module that contains a main implementation of NetCatKS logger
"""
from twisted.python import log
from zope.interface import implementer
from NetCatKS.Logger.api.interfaces import ILogger


__author__ = 'dimd'

GLOBAL_DEBUG = True


@implementer(ILogger)
class Logger(object):
    """
    A base NetCatKS logger
    """

    # NETODO to be improved

    @staticmethod
    def debug(msg):

        """
        Using for a debug messaging
        :param msg:
        :type msg: str

        :return: void
        """
        if GLOBAL_DEBUG is True:
            log.msg('[ ====== DEBUG ]: {}'.format(msg))

    @staticmethod
    def info(msg):

        """
        Using for a info messaging
        :param msg:
        :type msg: str

        :return: void
        """
        log.msg('[ ++++++ INFO ]: {}'.format(msg))

    @staticmethod
    def warning(msg):

        """
        Using for a warning messaging
        :param msg:
        :type msg: str

        :return: void
        """
        log.msg('[ !!!!!! WARNING ]: {}'.format(msg))

    @staticmethod
    def error(msg):
        """

        Using for a error messaging
        :param msg:
        :type msg: str

        :return: void
        """
        log.msg('[ ------ ERROR ]: {}'.format(msg))

    @staticmethod
    def critical(msg):

        """
        Using for a critical messaging
        :param msg:
        :type msg: str

        :return: void
        """
        log.msg('[ @@@@@@ CRITICAL ]: {}'.format(msg))


__all__ = [
    'Logger'
]
