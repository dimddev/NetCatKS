"""
A module that represent our default TCP live receiver protocol
"""

from twisted.protocols.basic import LineReceiver

from NetCatKS.NetCAT.api.interfaces.twisted.protocols.linereceiver import IDefaultLineReceiver

from NetCatKS.Dispatcher import IDispatcher, DispathcherResultHelper
from NetCatKS.Validators import Validator
from NetCatKS.Logger import Logger

from zope.interface import implementer

__author__ = 'dimd'


@implementer(IDefaultLineReceiver)
class DefaultLineReceiver(LineReceiver):
    """
    A default implementation of Twisted LineReceiver protocol
    """
    def __init__(self):
        """
        A constructor will init the logger only
        :return: void
        """
        self.__logger = Logger()

    def connectionMade(self):
        """
        A callback method that is fired when connection is made
        :return: void
        """
        self.__logger.info('Connections made')

    def connectionLost(self, reason='unexpected'):
        """
        A callback method that is fired when connection is lost
        :param reason:
        :return: void
        """
        self.__logger.info('Connection was closesd: {}'.format(reason))

    def lineReceived(self, line):
        """
        A callback method that is fired when live is received.
        Will validate, dispatch and choose the right API on the fly
        :param line: user input
        :type line: JSON or XML
        :return: void
        """
        self.__logger.info('Received line: {}'.format(line))

        result = IDispatcher(Validator(line)).dispatch()
        result_helper = DispathcherResultHelper(result)

        result_helper.result_validation(
            self.sendLine,
            self.transport.loseConnection,
            'TCP'
        )
