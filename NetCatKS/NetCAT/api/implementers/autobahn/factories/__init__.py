"""
A module that represent our default WAMP Factory
"""

import traceback

from autobahn.wamp.types import ComponentConfig

from autobahn.websocket.util import parse_url

from autobahn.twisted.websocket import WampWebSocketClientFactory

from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString
from twisted.application import service

from NetCatKS.Logger import Logger
from NetCatKS.NetCAT.api.public import IDefaultAutobahnFactory
from NetCatKS.NetCAT.api.implementers.autobahn.factories.ws import DefaultWSFactory
from NetCatKS.Config.api.implementers.configuration.wamp import WAMP

from zope.interface import implementer

__author__ = 'dimd'


class Reconnect(object):
    """
    A reconnect class
    """
    def __init__(self, **kwargs):
        """
        A constructor will init our wamp session and a runner.
        A runner is a callable that have to be processed when we lose the connection

        :param kwargs: keys: 'session' and 'runner'
        :return: void
        """

        if 'session' not in kwargs or 'runner' not in kwargs:
            raise Exception('session is not provided')

        self.__session = kwargs['session']
        self.__runner = kwargs['runner']

        self.logger = Logger()
        self.config = kwargs.get('config')

    def start(self):
        """
        Start the reconnection
        :return: void
        """
        try:

            self.logger.info(
                'TRYING TO CONNECT TO {}'.format(
                    self.config
                )
            )

            run = self.__runner(config=self.config)
            run.run(self.__session)

        except Exception as e:
            self.logger.error('RECONNECTING ERROR: {}'.format(e.message))


@implementer(IDefaultAutobahnFactory)
class AutobahnDefaultFactory(service.Service):
    """
    This class is a convenience tool mainly for development and quick hosting
    of WAMP application components.

    It can host a WAMP application component in a WAMP-over-WebSocket client
    connecting to a WAMP router.
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :type kwargs:
        """

        self.logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            self.config = {}
            wamp = WAMP()

            self.logger.warning('Config is not provided failback to defaults')

            self.config.update({
                'realm': 'realm1',
                'retry_interval': 2,  # in seconds
                'url': u'ws://localhost:8080/ws',
                'service_name': 'A Default WAMP Service name"'
            })

            self.config = wamp.to_object(self.config)

        self.url = kwargs.get('url', self.config.url)

        self.ssl = kwargs.get('ssl', None)

        self.is_secure, self.host, self.port, self.resource, self.path, self.params = parse_url(self.url)

        if self.is_secure and self.ssl is None:

            from twisted.internet._sslverify import OpenSSLCertificateAuthorities
            from twisted.internet.ssl import CertificateOptions
            from OpenSSL import crypto

            cert = crypto.load_certificate(
                crypto.FILETYPE_PEM,
                open(self.config.ssl.crt, 'r').read()
            )

            # tell Twisted to use just the one certificate we loaded to verify connections
            self.ssl = CertificateOptions(
                trustRoot=OpenSSLCertificateAuthorities([cert]),
            )

        self.realm = u'{}'.format(kwargs.get('realm', self.config.realm))

        self.extra = kwargs.get('extra', dict())

        self.belong_to = kwargs.get('belong_to', False)

        self.make = None

        # self.protocol = kwargs.get('protocol', self.config.protocol)

        self.name = kwargs.get('name', self.config.service.name)

        self.port = kwargs.get('port', self.port or self.config.port)

        self.host = kwargs.get('host', self.host or self.config.hostname)

        self.path = kwargs.get('path', self.path or self.config.path)

    def run(self, make):
        """
        Run the application component.

        :param make: A factory that produces instances of :class:`autobahn.asyncio.wamp.ApplicationSession`
           when called with an instance of :class:`autobahn.wamp.types.ComponentConfig`.
        :type make: callable
        """

        # factory for use ApplicationSession
        def create():
            """
            Will trying to create an ApplicationSession object
            :return: ApplicationSession
            """
            cfg = ComponentConfig(self.realm, self.extra)

            try:
                session = make(config=cfg)

            except Exception as e:

                # the app component could not be created .. fatal
                self.logger.critical('CREATE RUNNER EXCEPTION {}'.format(e.message))

            else:

                return session

        # create a WAMP-over-WebSocket transport client factory

        transport_factory = WampWebSocketClientFactory(
            create,
            url=self.url,
            serializers=None,
            proxy=None
        )

        # if user passed ssl= but isn't using isSecure, we'll never
        # use the ssl argument which makes no sense.
        context_factory = None
        if self.ssl is not None:

            if not self.is_secure:
                raise RuntimeError(
                    'ssl= argument value passed to %s conflicts with the "ws:" '
                    'prefix of the url argument. Did you mean to use "wss:"?' %
                    self.__class__.__name__)
            context_factory = self.ssl

        elif self.is_secure:

            from twisted.internet.ssl import optionsForClientTLS
            context_factory = optionsForClientTLS(self.host)

        if self.is_secure:

            from twisted.internet.endpoints import SSL4ClientEndpoint
            assert context_factory is not None
            client = SSL4ClientEndpoint(reactor, self.host, self.port, context_factory)

            endpoint_descriptor = "ssl:{0}:{1}".format(self.host, self.port)

        else:

            from twisted.internet.endpoints import TCP4ClientEndpoint
            client = TCP4ClientEndpoint(reactor, self.host, self.port)

            endpoint_descriptor = "tcp:{0}:{1}".format(self.host, self.port)

        try:
            self.logger.info('Trying to connect to: {}'.format(endpoint_descriptor))
            self.connect(client, transport_factory, make)

            return self

        except Exception as e:
            self.logger.error('CLIENT CONNECT ERROR: {}'.format(e.message))

    def connect(self, client, transport, session):
        """
        Will make a connection to a WAMP router based on a Twisted endpoint
        :param client:
        :param transport:
        :param session:
        :return:
        """
        try:

            # start the client from a Twisted endpoint

            # client = clientFromString(reactor, endpoint)

            res = client.connect(transport)

            def connect_result(result):
                """
                A callback used as defer result
                :param result:
                :return:
                """
                return result

            def connect_error(result):
                """
                A callback used as defer if error occur
                :param result:
                :return:
                """
                self.logger.error('CONNECTION ERROR: {}'.format(result.getErrorMessage()))

                try:

                    reconnect = Reconnect(
                        session=session,
                        runner=AutobahnDefaultFactory,
                        config=self.config
                    )

                    reactor.callLater(
                        self.config.retry_interval,
                        reconnect.start,
                    )

                except Exception as e:
                    self.logger.error('RECONNECTING ERROR: {}'.format(e.message))

            res.addCallback(connect_result)
            res.addErrback(connect_error)

            return res

        except Exception as e:
            self.logger.error('CONNECTION GLOBAL ERRORS: {}'.format(e.message))

    def startService(self):
        """
        Start a WAMP service
        :return:
        """
        service.Service.startService(self)

    def stopService(self):
        """
        Stop a WAMP service
        :return:
        """
        service.Service.stopService(self)


__all__ = [
    'AutobahnDefaultFactory',
    'Reconnect',
    'DefaultWSFactory'
]
