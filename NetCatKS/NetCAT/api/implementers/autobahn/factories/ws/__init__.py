__author__ = 'dimd'

from zope.interface import implementer

from twisted.internet.protocol import Factory
from autobahn.twisted.websocket import WebSocketServerFactory

from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory
from NetCatKS.NetCAT.api.implementers.autobahn.protocols import DefaultWSProtocol
from NetCatKS.Logger import Logger


@implementer(IDefaultWSFactory)
class DefaultWSFactory(WebSocketServerFactory):

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
                'port': 8484,
                'hostname': 'localhost',
                'protocol': 'ws'
            }

        self.protocol = kwargs.get('protocol', DefaultWSProtocol)

        self.name = kwargs.get('name', 'DefaultWSFactory')

        self.port = kwargs.get('port', self.config.get('port'))

        self.url = kwargs.get('port', self.config.get('url'))

        self.belong_to = kwargs.get('belong_to', False)

        super(DefaultWSFactory, self).__init__(
            self.url
        )
