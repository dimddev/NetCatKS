__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.registration.protocols import IProtocolRegister
from NetCatKS.Components.api.implementers.registration.factories import RegisterFactory
from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Dispatcher.api.interfaces import IJSONResource

from zope.interface import implementer

@implementer(IProtocolRegister)
class ProtocolRegister(RegisterFactory):

    def __init__(self, file_loader, session_source):

        super(ProtocolRegister, self).__init__(file_loader, session_source, [IJSONResource])

    def register_protocols(self):

        return self.register_factories()


class FileProtocolsLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Adapter"
        :param kwargs:
        :return:
        """
        super(FileProtocolsLoader, self).__init__(**kwargs)