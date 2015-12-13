"""
A module that represent our internal storage
"""

from zope.interface import implementer

from NetCatKS.Components.api.interfaces.storages import IStorageRegister
from NetCatKS.Components.common.factory import RegisterAsFactory

__author__ = 'dimd'


@implementer(IStorageRegister)
class StorageRegisterImplementer(object):
    """
    Internal storage used by our API's
    """
    __instance = None
    components = {}
    interfaces = {}

    def __new__(cls):
        """
        Implements a singleton pattern
        :return: void
        """

        if StorageRegisterImplementer.__instance is None:

            StorageRegisterImplementer.__instance = object.__new__(cls)

        return StorageRegisterImplementer.__instance


class StorageRegister(StorageRegisterImplementer):

    """
    A proxy class for our Storage. The users have to use this one
    """

    def __init__(self):
        """
        Just call a super
        :return: void
        """
        super(StorageRegister, self).__init__()

RegisterAsFactory(StorageRegister).register()

__all__ = ['StorageRegister']
