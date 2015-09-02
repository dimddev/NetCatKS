__author__ = 'dimd'

from twisted.application import service

from NetCatKS.NetCAT.api.implementers.autobahn.factories import AutobahnDefaultFactory
from NetCatKS.NetCAT.api.implementers.autobahn.components import WampDefaultComponent
from NetCatKS.NetCAT.api.interfaces.autobahn.services import IDefaultAutobahnService
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultAutobahnFactory

from zope.interface import implementer
from zope.component import adapts
from zope.component import getGlobalSiteManager


@implementer(IDefaultAutobahnService)
class DefaultAutobahnService(object):

    adapts(IDefaultAutobahnFactory)

    def __init__(self, factory):

        super(DefaultAutobahnService, self).__init__()

        self.factory = factory

        if self.factory.parent is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

    def start(self):

        adf = AutobahnDefaultFactory(
            url=u'%s://%s:%s/%s' % (
                self.factory.protocol,
                self.factory.host,
                self.factory.port,
                self.factory.path
            ),
            realm=u'%s' % self.factory.realm
        ).run(WampDefaultComponent)

        if self.factory.parent is False:

            adf.setServiceParent(self.service_collection)

            return self.__application

        else:

            adf.setServiceParent(self.factory.belong_to)
            return adf


gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultAutobahnService)


__all__ = [
    'DefaultAutobahnService'
]
