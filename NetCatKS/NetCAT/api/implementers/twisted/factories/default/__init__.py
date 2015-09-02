__author__ = 'dimd'

from zope.interface import implementer

from twisted.internet.protocol import Factory

from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultFactory
from NetCatKS.NetCAT.api.implementers.twisted.protocols.linereceiver import DefaultLineReceiver


@implementer(IDefaultFactory)
class DefaultFactory(Factory):

    def __init__(self, **kwargs):
        """
        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:
        :return:
        """
        self.protocol = kwargs.get('protocol', DefaultLineReceiver)

        self.name = kwargs.get('name', 'DefaultService')

        self.port = kwargs.get('port', 9999)

        self.belong_to = kwargs.get('belong_to', False)
