"""
Main storage of Dynamic Protocol API
"""

from NetCatKS.DProtocol.api.interfaces.storage import IProtocolStogareInterface
from zope.interface import implementer

__author__ = 'dimd'


@implementer(IProtocolStogareInterface)
class ProtocolStorageImplementor(object):

    """
    This storage having implement a singleton pattern.
    It's possible to be use only in a case when the protocol having implement id field
    """

    session = {}

    __instance = None

    def __new__(cls):

        """

        We having implement a singleton pattern for our Container to ensure that all commands point to one place
        :return: instance

        """

        if ProtocolStorageImplementor.__instance is None:

            ProtocolStorageImplementor.__instance = object.__new__(cls)

        return ProtocolStorageImplementor.__instance
