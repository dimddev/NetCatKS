"""
A module that care about creating of Web Socket servers
"""
from zope.interface import implementer
from autobahn.twisted.websocket import WebSocketServerFactory

from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory
from NetCatKS.NetCAT.api.implementers.autobahn.protocols import DefaultWSProtocol
from NetCatKS.Config.api.implementers.configuration.ws import WS
from NetCatKS.Logger import Logger
from autobahn.websocket.util import parse_url

__author__ = 'dimd'


class DefaultWSFactoryRunner(WebSocketServerFactory):

    """
    A Proxy class for a WS Factory
    """

    def __init__(self, *args, **kwargs):
        """

        Just call a super

        :param args:
        :param kwargs:

        :return:
        """
        super(DefaultWSFactoryRunner, self).__init__(*args, **kwargs)


@implementer(IDefaultWSFactory)
class DefaultWSFactory(object):

    """
    A class that represent a default WS Factory
    """

    def __init__(self, **kwargs):

        """
        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:

        :return:
        """
        self.__logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            ws = WS()

            self.__logger.warning('Config for IDefaultFactory is not provided, failback to defaults...')

            self.config = {
                'url': 'ws://localhost:8585',
                "service": {
                    "name": "DefaultWsServiceName"
                }
            }

            self.config = ws.to_object(self.config)

        self.is_secure, self.host, self.port, self.resource, self.path, self.params = parse_url(self.config.url)

        self.name = self.config.service.name

        self.url = self.config.url

        self.belong_to = kwargs.get('belong_to', False)

        self.ws_server_factory = DefaultWSFactoryRunner

        if self.is_secure == 'wss':

            key = self.config.ssl.key
            crt = self.config.ssl.crt

            if key is None or crt is None:
                raise AttributeError('WS over SSL required attribute a key and a crt')

            self.crt_keys = dict(key=key, crt=crt)

        self.ws_msg_protocol = DefaultWSProtocol
