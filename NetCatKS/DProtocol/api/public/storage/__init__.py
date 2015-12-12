"""
Public API for a ProtocolStorage
"""

from NetCatKS.DProtocol.api.implementors.storage import ProtocolStorageImplementor

__author__ = 'dimd'


class ProtocolStorage(ProtocolStorageImplementor):

    """
    A proxy class that have to be used by users
    """

    def __init__(self):

        """
        Just call the super constructor
        :return: void
        """

        super(ProtocolStorage, self).__init__()
