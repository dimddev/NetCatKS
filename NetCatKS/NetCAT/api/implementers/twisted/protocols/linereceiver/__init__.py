__author__ = 'dimd'

from NetCatKS.NetCAT.api.interfaces.twisted.protocols.linereceiver import IDefaultLineReceiver

from NetCatKS.Dispatcher import IDispatcher, IJSONResource, IXMLResourceAPI, IXMLResource
from NetCatKS.Validators import Validator, IValidator
from NetCatKS.Logger import Logger

from twisted.protocols.basic import LineReceiver
from zope.interface import implementer


@implementer(IDefaultLineReceiver)
class DefaultLineReceiver(LineReceiver):

    def __init__(self):

        self.__logger = Logger()

    def connectionMade(self):

        self.__logger.info('Connections made')

    def connectionLost(self, reason='unexpected'):

        self.__logger.info('Connection was closesd: {}'.format(reason))

    def lineReceived(self, line):

        self.__logger.info('Received line: {}'.format(line))

        result = IDispatcher(Validator(line)).dispatch()

        if IValidator.providedBy(result):

            self.__logger.warning('TCP Message is invalid: {}'.format(result.message))
            self.transport.loseConnection()

        else:

            if result:

                self.__logger.info('Response: {}'.format(result))

                if IJSONResource.providedBy(result):

                    self.sendLine(result.to_json())

                elif IXMLResource.providedBy(result):

                    self.sendLine(str(result.to_xml()))

            else:

                self.__logger.warning('TCP: This message was not be dispatched')
                self.transport.loseConnection()