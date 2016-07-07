"""
A module that contains functionality for our default TCP factory
"""
from zope.interface import implementer

from twisted.internet.protocol import Factory, ClientFactory

from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultFactory
from NetCatKS.NetCAT.api.implementers.twisted.protocols.linereceiver import DefaultLineReceiver
from NetCatKS.Config.api.implementers.configuration.tcp import TCP
from NetCatKS.Logger import Logger

__author__ = 'dimd'


class DefaultBaseTCPFactory(object):

    def __init__(self, **kwargs):
        """
        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:

        """

        self.__logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:
            self.__logger.warning('Config for IDefaultFactory is not provided, failback to defaults...')

            tcp = TCP()

            self.config = {
                'type': 'server',
                'hostname': '127.0.0.1',
                'port': 8484,
                'tcp_back_log': 50,
                'service': {
                    'name': 'Default TCP Server'
                }
            }

            self.config = tcp.to_object(self.config)

        self.protocol = kwargs.get('protocol', DefaultLineReceiver)

        self.name = self.config.service.name

        self.port = self.config.port

        self.belong_to = kwargs.get('belong_to', False)

        self.type = self.config.type

        self.hostname = self.config.hostname


@implementer(IDefaultFactory)
class DefaultFactory(DefaultBaseTCPFactory, Factory):
    """
    A default TCP Factory
    """
    def __init__(self, **kwargs):
        super(DefaultFactory, self).__init__(**kwargs)


@implementer(IDefaultFactory)
class DefaultClientFactory(DefaultBaseTCPFactory, ClientFactory):
    """
    A default TCP Factory
    """
    def __init__(self, **kwargs):
        super(DefaultClientFactory, self).__init__(**kwargs)

