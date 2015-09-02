__author__ = 'dimd'

from zope.interface import implementer

from twisted.internet.protocol import Factory

from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultFactory
from NetCatKS.NetCAT.api.implementers.twisted.protocols.linereceiver import DefaultLineReceiver
from NetCatKS.Logger import Logger

@implementer(IDefaultFactory)
class DefaultFactory(Factory):

    def __init__(self, **kwargs):
        """
        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:
        :return:
        """
        self.__logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            self.__logger.warning('Config for IDefaultFactory is not provided, failback to defaults...')

            self.config = {
                'TCP': {
                    'TCP_PORT': 8484,
                    'TCP_BACK_LOG': 50,
                    'TCP_SERVICE_NAME': 'Default TCP Server'
                }
            }

        self.protocol = kwargs.get('protocol', DefaultLineReceiver)

        self.name = kwargs.get('name', self.config.get('TCP_SERVICE_NAME'))

        self.port = kwargs.get('port', self.config.get('TCP_PORT'))

        self.belong_to = kwargs.get('belong_to', False)
