__author__ = 'dimd'

from zope.interface import implementer

from twisted.internet.protocol import Factory

from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultWebFactory
from NetCatKS.Logger import Logger


@implementer(IDefaultWebFactory)
class DefaultWebFactory(Factory):

    def __init__(self, **kwargs):

        """

        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:

        """
        self.__logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            self.__logger.warning('Config for IDefaultWebFactory is not provided, failback to defaults...')

            self.config = {
                'port': 8000,
                'www_root': '',
                'service_name': 'Default WEB Server',
                'http_methods': ['GET']
            }

        self.name = kwargs.get('name', self.config.get('service_name'))
        self.port = kwargs.get('port', self.config.get('port'))
        self.methods = kwargs.get('methods', self.config.get('http_methods'))
        self.belong_to = kwargs.get('belong_to', False)
