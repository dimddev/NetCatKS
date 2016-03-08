"""
A Default implementation of WS protocol
"""

from zope.interface import implementer
from autobahn.twisted.websocket import WebSocketServerProtocol

from NetCatKS.NetCAT.api.interfaces import IWSProtocol
from NetCatKS.Dispatcher import IDispatcher, DispathcherResultHelper
from NetCatKS.Validators import Validator
from NetCatKS.Logger import Logger


__author__ = 'dimd'


logger = Logger()


@implementer(IWSProtocol)
class DefaultWSProtocol(WebSocketServerProtocol):
    """
    A class that implements a Default WS Protocol
    """
    def onConnect(self, request):

        """
        A callback that fired when connect occur
        :param request:

        :return:
        """
        logger.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):

        """
        A callback when onOpen event is happen

        :return:
        """
        logger.info("WebSocket connection open.")

    def onMessage(self, payload, is_binary):

        """
        A callback that fired when message is arrived
        :param payload:
        :param is_binary:

        :return:
        """
        if is_binary:

            logger.info("Binary message received: {0} bytes".format(len(payload)))
            self.dropConnection('not supported')

        else:

            result = IDispatcher(Validator(payload.decode('utf8'))).dispatch()
            result_helper = DispathcherResultHelper(result)

            result_helper.result_validation(
                self.sendMessage,
                self.dropConnection,
                'WS'
            )

    def onClose(self, was_clean, code, reason):
        """
        A close callback, it's fired when onClose event is happen
        :param was_clean:
        :param code:
        :param reason:
        :return:
        """
        logger.info("WebSocket connection closed: {0}".format(reason))
