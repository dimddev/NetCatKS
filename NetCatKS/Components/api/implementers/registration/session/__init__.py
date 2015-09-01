__author__ = 'dimd'

from .....api.interfaces.registration.session import ISessionRegister
from .....api.implementers.registration.factories import RegisterFactory
from .....common.loaders import BaseLoader

from zope.interface import implementer

@implementer(ISessionRegister)
class SessionRegister(RegisterFactory):

    def __init__(self, file_loader, session_source):
        super(SessionRegister, self).__init__(file_loader, session_source)

    def register_sessions(self):

        return self.register_factories()


class FileSessionsLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Adapter"
        :param kwargs:
        :return:
        """
        super(FileSessionsLoader, self).__init__(**kwargs)