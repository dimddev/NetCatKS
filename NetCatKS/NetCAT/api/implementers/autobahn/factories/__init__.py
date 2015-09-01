__author__ = 'dimd'

import sys

#run
from autobahn.wamp.types import ComponentConfig
from autobahn.websocket.protocol import parseWsUrl
from autobahn.twisted.websocket import WampWebSocketClientFactory
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString
from twisted.application import service

from NetCatKS.Logger import Logger

WEB_SERVICE_PROTO = 'wss'
WEB_SERVICE_IP = '144.76.33.119'
WEB_SERVICE_PORT = '8080'
WEB_SERVICE_REALM = 'realm1'
WEB_SERVICE_PATH = 'ws'
WEB_SERVICE_RETRY_INTERVAL = 2  # in seconds


class Reconnect(object):

    def __init__(self, **kwargs):

        if 'session' not in kwargs or 'runner' not in kwargs:
            raise Exception('session is not provided')

        self.__session = kwargs['session']
        self.__runner = kwargs['runner']

        self.logger = Logger()

    def start(self):

        try:

            self.logger.info(
                'TRY TO CONNECT TO {}://{}:{}/{}'.format(
                    WEB_SERVICE_PROTO,
                    WEB_SERVICE_IP,
                    WEB_SERVICE_PORT,
                    WEB_SERVICE_PATH
            ))

            run = self.__runner(
                url=u'{}://{}:{}/{}'.format(WEB_SERVICE_PROTO, WEB_SERVICE_IP, WEB_SERVICE_PORT, WEB_SERVICE_PATH),
                realm=u'{}'.format(WEB_SERVICE_REALM)
            )
            run.run(self.__session)

        except Exception as e:
            self.logger.error('RECONNECTING ERROR: {}'.format(e.message))


class AutobahnDefaultFactory(service.Service):
    """
    This class is a convenience tool mainly for development and quick hosting
    of WAMP application components.

    It can host a WAMP application component in a WAMP-over-WebSocket client
    connecting to a WAMP router.
    """

    def __init__(self, url, realm, extra=None, debug=False, debug_wamp=False, debug_app=False):
        """

        :param url: The WebSocket URL of the WAMP router to connect to (e.g. `ws://somehost.com:8090/somepath`)
        :type url: unicode
        :param realm: The WAMP realm to join the application session to.
        :type realm: unicode
        :param extra: Optional extra configuration to forward to the application component.
        :type extra: dict
        :param debug: Turn on low-level debugging.
        :type debug: bool
        :param debug_wamp: Turn on WAMP-level debugging.
        :type debug_wamp: bool
        :param debug_app: Turn on app-level debugging.
        :type debug_app: bool
        """
        self.url = url
        self.realm = realm
        self.extra = extra or dict()
        self.debug = debug
        self.debug_wamp = debug_wamp
        self.debug_app = debug_app
        self.make = None
        self.logger = Logger()

    def run(self, make):
        """
        Run the application component.

        :param make: A factory that produces instances of :class:`autobahn.asyncio.wamp.ApplicationSession`
           when called with an instance of :class:`autobahn.wamp.types.ComponentConfig`.
        :type make: callable
        """

        isSecure, host, port, resource, path, params = parseWsUrl(self.url)

        ## start logging to console
        if self.debug or self.debug_wamp or self.debug_app:
            log.startLogging(sys.stdout)

        ## factory for use ApplicationSession
        def create():

            cfg = ComponentConfig(self.realm, self.extra)

            try:
                session = make(cfg)

            except Exception as e:

                ## the app component could not be created .. fatal
                self.logger.critical('CREATE RUNNER EXCEPTION {}'.format(e.message))
                log.err()
                #reactor.stop()

            else:
                session.debug_app = self.debug_app
                return session

        ## create a WAMP-over-WebSocket transport client factory
        transport_factory = WampWebSocketClientFactory(
            create,
            url=self.url,
            debug=self.debug,
            debug_wamp=
            self.debug_wamp
        )

        if isSecure:
            endpoint_descriptor = "ssl:{0}:{1}".format(host, port)

        else:
            endpoint_descriptor = "tcp:{0}:{1}".format(host, port)

        try:

            self.connect(endpoint_descriptor, transport_factory, make)

            return self

        except Exception as e:
            self.logger.error('CLIENT CONNECT ERROR: {}'.format(e.message))

    def connect(self, endpoint, transport, session):

        try:
            ## start the client from a Twisted endpoint

            client = clientFromString(reactor, endpoint)

            res = client.connect(transport)

            def connect_result(result):
                return result

            def connect_error(result):

                self.logger.error('CONNECTION ERROR: {}'.format(result.getErrorMessage()))

                try:

                    reconnect = Reconnect(session=session, runner=AutobahnDefaultFactory)

                    reactor.callLater(
                        WEB_SERVICE_RETRY_INTERVAL,
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
        service.Service.startService(self)

    def stopService(self):
        service.Service.stopService(self)

__all__ = [
    'AutobahnDefaultFactory'
]
