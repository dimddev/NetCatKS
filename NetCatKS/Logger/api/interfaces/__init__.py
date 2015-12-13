"""
A module that contains the interfaces which describing our Logger API
"""
from zope.interface import Interface, Attribute
__author__ = 'dimd'


class ILogger(Interface):

    """
    A Base logger interface
    """

    default = Attribute("default logging module")
    origin = Attribute("Current module")

    def info(msg):
        """
        Info logging level
        :param msg: info message
        """

    def debug(msg):
        """
        debug logging level
        :param msg: debug message
        """

    def error(msg):
        """
        error level logging
        :param msg: error message
        :return:
        """

    def warning(msg):
        """
        warning level logging
        :param msg: warrning message
        :return:
        """

    def critical(msg):
        """
        critical logging level
        :param msg:
        :return:
        """
