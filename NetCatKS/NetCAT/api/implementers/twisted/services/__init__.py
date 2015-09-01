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

        self.__factory = factory

        self.__application = service.Application(self.__factory.name, uid=1000, gid=1000)
        self.__service_collection = service.IServiceCollection(self.__application)

    def start(self):

        internet.TCPServer(
            self.__factory.port,
            self.__factory,
            50
        ).setServiceParent(self.__service_collection)

        return self.__application


gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultService)


__all__ = [
    'DefaultService'
]
