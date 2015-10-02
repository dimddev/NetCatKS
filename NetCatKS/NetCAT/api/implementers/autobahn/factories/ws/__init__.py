__author__ = 'dimd'

from zope.interface import implementer

from twisted.internet.protocol import Factory
from autobahn.twisted.websocket import WebSocketServerFactory

from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory
from NetCatKS.NetCAT.api.implementers.autobahn.protocols import DefaultWSProtocol
from NetCatKS.Logger import Logger


@implementer(IDefaultWSFactory)
class DefaultWSFactory(object):

    def __init__(self, **kwargs):
        """
        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:
        :return:
        """
        self.__logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            self.__logger.warning('Config for IDefaultFactory is not provided, failback to defaults...')

            self.config = {
                'url': 'ws://localhost:8585',
                'port': 8585,
                'hostname': 'localhost',
                'protocol': 'ws'
            }

        self.ws_protocol = self.config.get('protocol', 'ws')

        self.name = kwargs.get('name', 'DefaultWSFactory')

        self.port = kwargs.get('port', self.config.get('port'))

        self.url = kwargs.get('port', self.config.get('url').decode('utf8'))

        self.belong_to = kwargs.get('belong_to', False)

        self.ws_server_factory = WebSocketServerFactory

        if self.ws_protocol == 'wss':

            key = self.config.get('keys').get('key', None)
            crt = self.config.get('keys').get('crt', None)

            if key is None or crt is None:
                raise AttributeError('WS over SSL required attribute key and crt')

            self.crt_keys = dict(key=key, crt=crt)


        self.ws_msg_protocol = DefaultWSProtocol