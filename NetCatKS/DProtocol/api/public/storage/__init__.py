__author__ = 'dimd'

from NetCatKS.DProtocol.api.implementors.storage import SessionStorageImplementor


class ProtocolStorage(SessionStorageImplementor):
    def __init__(self):
        super(ProtocolStorage, self).__init__()