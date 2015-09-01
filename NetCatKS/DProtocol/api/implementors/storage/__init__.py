__author__ = 'dimd'

from ...interfaces.storage import IProtocolStogareInterface
from zope.interface import implementer


@implementer(IProtocolStogareInterface)
class SessionStorageImplementor(object):

    session = {}

    __instance = None

    def __new__(cls):
        """
        we implement singleton patter for our Container to ensure that all commands point to one place

        :param cls:
            self instance
        :return:
            singleton instance
        """

        if SessionStorageImplementor.__instance is None:

            SessionStorageImplementor.__instance = object.__new__(cls)

        return SessionStorageImplementor.__instance
