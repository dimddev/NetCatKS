__author__ = 'dimd'

from datetime import datetime

from twisted.application import internet, service
from twisted.internet import ssl

from zope.interface import classImplementsOnly
from zope.component import adapts
from zope.component import getGlobalSiteManager

from NetCatKS.NetCAT.api.interfaces.autobahn.services import IDefaultWSService
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory
from NetCatKS.Logger import Logger

from autobahn.twisted.websocket import listenWS


class DefaultWSService(service.Service):
    """
    Provides functionality for starting default TCP Server as single app or as part of many services
    """
    adapts(IDefaultWSFactory)

    def __init__(self, factory):
        """

        :param factory:
        :type IDefaultFactory

        """
        super(DefaultWSService, self).__init__()

        self.factory = factory
        self.__logger = Logger()

        if self.factory.ws_protocol == 'wss':

            print('{} [ NetCatKS ] {} entering secure mode'.format(
                datetime.now(), self.factory.name
            ))

            self.__ssl_context = ssl.DefaultOpenSSLContextFactory(
                self.factory.crt_keys.get('key'),
                self.factory.crt_keys.get('crt')
            )

        if self.factory.belong_to is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

        else:

            self.service_collection = self.factory.belong_to

    def start(self):

        """
        Starting a TCP server and put to the right service collection

        :return:
        """
        if self.factory.ws_protocol == 'ws':

            internet.TCPServer(
                self.factory.port,
                self.factory.ws_server_factory,
                50
            ).setServiceParent(self.service_collection)

        else:

            listenWS(self.factory.ws_server_factory, self.__ssl_context)

            print('{} [ NetCatKS ] DefaultWSFactory starting on {} mode secure (WS over SSL)'.format(
                datetime.now(),
                self.factory.port
            ))

        if self.factory.belong_to is False:

            return self.__application


classImplementsOnly(DefaultWSService, IDefaultWSService)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultWSService)


__all__ = [
    'DefaultWSService'
]
