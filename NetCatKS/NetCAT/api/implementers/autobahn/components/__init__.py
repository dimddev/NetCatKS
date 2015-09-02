__author__ = 'dimd'

from zope.interface import implementer

from NetCatKS.NetCAT.api.implementers.autobahn.factories import AutobahnDefaultFactory, Reconnect
from NetCatKS.NetCAT.api.interfaces.autobahn.components import IWampDefaultComponent
from NetCatKS.Logger import Logger

from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor

WEB_SERVICE_RETRY_INTERVAL = 2


@implementer(IWampDefaultComponent)
class WampDefaultComponent(ApplicationSession):

    def __init__(self, config=None):
        super(WampDefaultComponent, self).__init__(config)
        self.__logger = Logger()

    @inlineCallbacks
    def onJoin(self, details):
        self.__logger.info('WAMP Session is ready')
        yield

    def onDisconnect(self):

        self.__logger.warning('Disconnected...')

        try:

            reconnect = Reconnect(session=WampDefaultComponent, runner=AutobahnDefaultFactory)

            reactor.callLater(
                WEB_SERVICE_RETRY_INTERVAL,
                reconnect.start,
            )

        except Exception as e:
            self.__logger.warning('disconnect warn: {}'.format(e.message))


__all__ = [
    'WampDefaultComponent'
]