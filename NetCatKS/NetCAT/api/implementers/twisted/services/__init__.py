__author__ = 'dimd'

from twisted.application import internet, service

from zope.interface import implementer
from zope.component import adapts
from zope.component import getGlobalSiteManager

from NetCatKS.NetCAT.api.interfaces.twisted.services import IDefaultService
from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultFactory


@implementer(IDefaultService)
class DefaultService(object):

    adapts(IDefaultFactory)

    def __init__(self, factory):

        super(DefaultService, self).__init__()

        self.factory = factory

        if self.factory.belong_to is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

        else:

            self.service_collection = self.factory.belong_to

    def start(self):

        tcp = internet.TCPServer(
            self.factory.port,
            self.factory,
            50
        ).setServiceParent(self.service_collection)

        if self.factory.belong_to is False:

            return self.__application

        else:
            return tcp


gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultService)


__all__ = [
    'DefaultService'
]
