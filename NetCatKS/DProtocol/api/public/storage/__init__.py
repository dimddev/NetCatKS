__author__ = 'dimd'

from ...implementors.storage import SessionStorageImplementor


class ProtocolStorage(SessionStorageImplementor):
    def __init__(self):
        super(ProtocolStorage, self).__init__()