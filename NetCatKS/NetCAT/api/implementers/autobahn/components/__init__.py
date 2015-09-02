__author__ = 'dimd'

from zope.interface import implementer

from NetCatKS.NetCAT.api.implementers.autobahn.factories import AutobahnDefaultFactory, Reconnect
from NetCatKS.NetCAT.api.interfaces.autobahn.components import IWampDefaultComponent
from NetCatKS.Logger import Logger
from NetCatKS.Config import Config

from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor


@implementer(IWampDefaultComponent)
class WampDefaultComponent(ApplicationSession):

    def __init__(self, config=None):

        super(WampDefaultComponent, self).__init__(config)

        self.__logger = Logger()
        self.cfg = Config()

    @inlineCallbacks
    def onJoin(self, details):
        self.__logger.info('WAMP Session is ready')
        yield

    def onDisconnect(self):

        self.__logger.warning('Disconnected...')

        try:

            reconnect = Reconnect(
                session=WampDefaultComponent,
                runner=AutobahnDefaultFactory,
                config=self.cfg.get('WAMP')
            )

            reactor.callLater(
                self.cfg.get('WAMP').get('WS_RETRY_INTERVAL'),
                reconnect.start,
            )

        except Exception as e:
            self.__logger.warning('disconnect warn: {}'.format(e.message))


__all__ = [
    'WampDefaultComponent'
]