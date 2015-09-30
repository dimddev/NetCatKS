__author__ = 'dimd'

from twisted.application import internet, service

from zope.interface import classImplementsOnly
from zope.component import adapts
from zope.component import getGlobalSiteManager

from NetCatKS.NetCAT.api.interfaces.autobahn.services import IDefaultWSService
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory


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
        internet.TCPServer(
            self.factory.port,
            self.factory,
            50
        ).setServiceParent(self.service_collection)

        if self.factory.belong_to is False:

            return self.__application


classImplementsOnly(DefaultWSService, IDefaultWSService)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultWSService)


__all__ = [
    'DefaultWSService'
]
