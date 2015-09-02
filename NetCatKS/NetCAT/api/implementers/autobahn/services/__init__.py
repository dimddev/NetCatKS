__author__ = 'dimd'

from twisted.application import service

from NetCatKS.NetCAT.api.implementers.autobahn.components import WampDefaultComponent
from NetCatKS.NetCAT.api.interfaces.autobahn.services import IDefaultAutobahnService
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultAutobahnFactory

from zope.interface import implementer
from zope.component import adapts
from zope.component import getGlobalSiteManager


@implementer(IDefaultAutobahnService)
class DefaultAutobahnService(object):

    """

    Default Autobahn Service, designed for single and multi service usage
    The class adapts IDefaultAutobahnFactory

    """

    adapts(IDefaultAutobahnFactory)

    def __init__(self, factory):

        """
        The constructor will prepare single or multi service,
        if self.factory.belong_to is not False, meaning we have to
        start multi services

        :param factory: IDefaultAutobahnFactory implementation
        :return:
        """

        super(DefaultAutobahnService, self).__init__()

        self.factory = factory

        if self.factory.belong_to is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

    def start(self):
        """
        Will attach WampDefaultComponent component through AutobahnDefaultFactory
        to our service parent, if self.factory.belong_to is not False will be multi service,
        otherwise - single service
        :return: if service is multi will return the AutobahnDefaultFactory instance otherwise
        twisted application instance
        """
        adf = self.factory.run(WampDefaultComponent)

        if self.factory.belong_to is False:

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