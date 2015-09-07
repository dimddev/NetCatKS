__author__ = 'dimd'

from NetCatKS.Dispatcher import IJSONResource, IJSONResourceAPI
from zope.interface import implementer
from zope.component import adapts, getGlobalSiteManager
from NetCatKS.Logger import Logger

log = Logger()

@implementer(IJSONResourceAPI)
class Command(object):

    adapts(IJSONResource)

    def __init__(self, factory):
        self.factory = factory

    def event(self):

        log.info('TIME API ADAPTER: {}'.format(self.factory.id))
        self.factory.id = 10
        return self.factory


@implementer(IJSONResourceAPI)
class Convert(object):

    adapts(IJSONResource)

    def __init__(self, factory):

        self.factory = factory

    def process_factory(self):

        self.factory.convert.id = 4200
        return self.factory


gsm = getGlobalSiteManager()

gsm.registerSubscriptionAdapter(Convert)
gsm.registerSubscriptionAdapter(Command)