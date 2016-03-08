"""
A module that contains a WAMP functionality
"""
from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component import subscribers, createObject

from autobahn.wamp import auth
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor

from NetCatKS.NetCAT.api.implementers.autobahn.factories import AutobahnDefaultFactory, Reconnect
from NetCatKS.NetCAT.api.interfaces.autobahn.components import IWampDefaultComponent
from NetCatKS.Components import IWAMPResource, IUserGlobalSubscriber, IJSONResource, IWAMPLoadOnRunTime
from NetCatKS.Logger import Logger
from NetCatKS.Config import Config
from NetCatKS.Dispatcher import IDispatcher
from NetCatKS.Validators import Validator, IValidator


__author__ = 'dimd'


def on_connect(self):
    """
    A function that is called when we got connected to a WAMP router.
    This function is attached to our WampDefaultComponent only if protocol is WSS
    :param self:
    :return: void
    """
    cfg = Config().get_wamp()
    log = Logger()

    log.info('Connecting to router...')

    self.join(self.config.realm, [u'wampcra'], cfg.user)


def on_challenge(self, challenge):

    """
    A function that is called when we got onChallenge event aka authentication to a WAMP router.
    This function is attached to our WampDefaultComponent only if protocol is WSS

    :param self:
    :param challenge:

    :return: digital signature decode in ascii
    """

    log = Logger()
    log.info('On Challenge...')

    if challenge.method == u"wampcra":

        cfg = Config().get_wamp()

        password = {
            u'%s' % cfg.user: u'%s' % cfg.password
        }

        if u'salt' in challenge.extra:

            key = auth.derive_key(
                password[cfg.user].encode('utf8'),
                challenge.extra['salt'].encode('utf8'),
                challenge.extra.get('iterations', None),
                challenge.extra.get('keylen', None)
            )

        else:

            key = password[cfg.user].encode('utf8')
        
        signature = auth.compute_wcs(key, challenge.extra['challenge'].encode('utf8'))

        return signature.decode('ascii')

    else:

        raise Exception("don't know how to compute challenge for authmethod {}".format(challenge.method))


@implementer(IWampDefaultComponent)
class WampDefaultComponent(ApplicationSession):

    """
    Class that represent our default WAMP component we inherit from
    autobahn.twisted.wamp.ApplicationSession
    """

    def __init__(self, **kwargs):
        """
        The constructor will init self.cfg self.__gsm and if the protocol is wss,
        will attach on_connect and on_challenge to this object as methods
        :param kwargs: we looking for key 'config'
        :return: void
        """
        config = kwargs.get('config')

        super(WampDefaultComponent, self).__init__(config)

        self.__logger = Logger()
        self.cfg = Config().get_wamp()

        self.__gsm = getGlobalSiteManager()

        if self.cfg.protocol == 'wss':

            self.__logger.info('WAMP is secure, switch to wss...')

            WampDefaultComponent.onConnect = on_connect
            WampDefaultComponent.onChallenge = on_challenge

    def subscriber_dispatcher(self, sub_data):

        """
        Callback function for our global subscriber
        will pass sub_data to GlobalSubscribeMessage and then will trying to
        get wamp component which implements IUserGlobalSubscriber and adapts
        IGlobalSubscribeMessage

        :param sub_data:
        """

        log = Logger()

        try:

            result = IDispatcher(Validator(sub_data)).dispatch()

        # NETODO what exception can happen here?
        except Exception as e:

            import traceback
            print traceback.format_exc()

            log.warning('subscriber_dispatcher exception: {}'.format(
                e.message
            ))

        else:

            if IValidator.providedBy(result):
                log.warning('WAMP Message is invalid: {}'.format(result.message))

            if result is not False and IJSONResource.providedBy(result):

                fac = None

                for sub in subscribers([result], IUserGlobalSubscriber):

                    sub.subscribe(self)
                    fac = True

                    break

                if not fac:
                    log.warning('There are no user definition for IUserGlobalSubscriber, message was skipped')



    @inlineCallbacks
    def onJoin(self, details):
        """
        Autobahn callback function that fired when onJoin happens (we join to our realm)

        Here all components recognized as WAMP we will registering on the fly.

        The global subscriber will be started too, its name is formed by
        netcatks_global_subscriber_ + WAMP Service name.

        Also inside our Storage register will be saved the current WAMP session object
        in __wamp_session__ namespace.

        If there an API which providing a IWAMPLoadOnRunTime implementation will be started on
        run time

        :param details:
        :return:
        """
        self.__logger.info('WAMP Session is ready')

        sub_topic = 'netcatks_global_subscriber_{}'.format(
            self.cfg.service_name.lower().replace(' ', '_')
        )

        yield self.subscribe(self.subscriber_dispatcher, sub_topic)
        self.__logger.info('Starting global subscriber: {}'.format(sub_topic))

        # registration of all classes which ends with Wamp into shared wamp session
        for x in list(self.__gsm.registeredSubscriptionAdapters()):

            # storing wamp session inside storage
            sr = createObject('storageregister').components
            sr['__wamp_session__'] = self

            if IWAMPResource in x.required:

                if x.factory.__name__ != 'BaseWampComponent':

                    f = x.factory()

                    self.__logger.info('Register Wamp Component: {}'.format(f.__class__.__name__))

                    yield self.register(f)

                    # here we provide wamp session to each wamp component,
                    # in this way every component can access methods like publish, call etc,
                    # which are hosted by default inside wamp session.

                    f.set_session(self)

            if x.provided is IWAMPLoadOnRunTime:
                x.factory('init').load()

    def onDisconnect(self):

        """
        Will be fired when we go a disconnecting from a WAMP router
        :return:
        """
        self.__logger.warning('Disconnected...')

        try:

            reconnect = Reconnect(
                session=WampDefaultComponent,
                runner=AutobahnDefaultFactory,
                config=self.cfg
            )

            reactor.callLater(
                self.cfg.retry_interval,
                reconnect.start,
            )

        # NETODO what exception trow here?
        except Exception as e:
            self.__logger.warning('disconnect warn: {}'.format(e.message))


__all__ = [
    'WampDefaultComponent'
]
