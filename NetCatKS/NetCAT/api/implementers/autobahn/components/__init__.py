__author__ = 'dimd'

from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component import subscribers

from NetCatKS.NetCAT.api.implementers.autobahn.factories import AutobahnDefaultFactory, Reconnect
from NetCatKS.NetCAT.api.interfaces.autobahn.components import IWampDefaultComponent
from NetCatKS.NetCAT.api.interfaces import IGlobalSubscriberCallback
from NetCatKS.Components import IWAMPResource
from NetCatKS.Logger import Logger
from NetCatKS.Config import Config
from NetCatKS.Dispatcher import IDispatcher
from NetCatKS.Validators import Validator, IValidator

from autobahn.wamp import auth
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor


def onConnect(self):

    cfg = Config().get('WAMP')
    log = Logger()

    log.info('Connecting to router...')

    self.join(self.config.realm, [u'wampcra'], cfg.get('WS_USER'))


def onChallenge(self, challenge):

    log = Logger()
    log.info('On Challenge...')

    if challenge.method == u"wampcra":

        cfg = Config().get('WAMP')

        password = {
            u'%s' % cfg.get('WS_USER'): u'%s' % cfg.get('WS_PASS')
        }

        if u'salt' in challenge.extra:

            key = auth.derive_key(
                password[cfg.get('WS_USER')].encode('utf8'),
                challenge.extra['salt'].encode('utf8'),
                challenge.extra.get('iterations', None),
                challenge.extra.get('keylen', None)
            )

        else:
            key = password[cfg.get('WS_USER')].encode('utf8')

        signature = auth.compute_wcs(key, challenge.extra['challenge'].encode('utf8'))

        return signature.decode('ascii')

    else:

        raise Exception("don't know how to compute challenge for authmethod {}".format(challenge.method))


def subscriber_dispatcher(sub_data):

    """
    Callback function for our global subscriber
    will pass sub_data to GlobalSubscribeMessage and then will trying to
    get wamp component which implements IGlobalSubscriberCallback and adapts
    IGlobalSubscribeMessage

    :param sub_data:
    """

    log = Logger()

    result = IDispatcher(Validator(sub_data)).dispatch()

    if IValidator.providedBy(result):
        log.warning('WAMP Message is invalid: {}'.format(result.message))

    else:

        if result is not False:

            log.info('Incoming message to global subscriber: {}'.format(result.to_dict()))

            fac = None

            for sub in subscribers([result], IGlobalSubscriberCallback):

                sub.subscribe()
                fac = True

                break

            if not fac:
                log.warning('There are no user definition for IGlobalSubscriberCallback, message was skipped')


@implementer(IWampDefaultComponent)
class WampDefaultComponent(ApplicationSession):

    def __init__(self, **kwargs):

        config = kwargs.get('config')

        super(WampDefaultComponent, self).__init__(config)

        self.__logger = Logger()
        self.cfg = Config()

        self.__gsm = getGlobalSiteManager()

        if self.cfg.get('WAMP').get('WS_PROTO') == 'wss':

            self.__logger.info('WAMP is secure, switch to wss...')

            WampDefaultComponent.onConnect = onConnect
            WampDefaultComponent.onChallenge = onChallenge

    @inlineCallbacks
    def onJoin(self, details):

        self.__logger.info('WAMP Session is ready')

        # registration of all classes which ends with Wamp into shared wamp session
        for x in list(self.__gsm.registeredSubscriptionAdapters()):

            # only if class implements IWAMPResource will be register as RPC
            # IWAMPResource means RPC

            if IWAMPResource in x.required:

                f = x.factory()

                self.__logger.info('Register Wamp Component: {}'.format(f.__class__.__name__))

                yield self.register(f)

                # here we provide wamp session to each wamp component,
                # in this way every component can access methods like publish, call etc,
                # which are hosted by default inside wamp session.

                f.set_session(self)

        sub_topic = 'netcatks_global_subscriber_{}'.format(
            self.cfg.get('WAMP').get('WS_NAME').lower().replace(' ', '_')
        )

        yield self.subscribe(subscriber_dispatcher, sub_topic)
        self.__logger.info('Starting global subscriber: {}'.format(sub_topic))

    def onDisconnect(self):
        """

        :return:
        """
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