__author__ = 'dimd'

from .....api.interfaces.registration.session import IProtocolRegister
from .....api.implementers.registration.factories import RegisterFactory
from .....common.loaders import BaseLoader

from zope.interface import implementer

@implementer(IProtocolRegister)
class ProtocolRegister(RegisterFactory):

    def __init__(self, file_loader, session_source):
        super(ProtocolRegister, self).__init__(file_loader, session_source)

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