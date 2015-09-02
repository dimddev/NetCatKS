__author__ = 'dimd'

from zope.interface import implementer
from zope.component import getGlobalSiteManager


from NetCatKS.NetCAT.api.implementers.autobahn.factories import AutobahnDefaultFactory, Reconnect
from NetCatKS.NetCAT.api.interfaces.autobahn.components import IWampDefaultComponent
from NetCatKS.Components import IWAMPResource
from NetCatKS.Logger import Logger
from NetCatKS.Config import Config

from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor


@implementer(IWampDefaultComponent)
class WampDefaultComponent(ApplicationSession):

    def __init__(self, **kwargs):

        config = kwargs.get('config')

        super(WampDefaultComponent, self).__init__(config)

        self.__logger = Logger()
        self.cfg = Config()

        self.__gsm = getGlobalSiteManager()

    @inlineCallbacks
    def onJoin(self, details):

        self.__logger.info('WAMP Session is ready')

        for x in list(self.__gsm.registeredSubscriptionAdapters()):

            if IWAMPResource in x.required:

                f = x.factory()

                self.__logger.info('Register Wamp Component: {}'.format(f.__class__.__name__))

                yield self.register(f)

                f.set_session(self)

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