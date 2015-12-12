"""
A Base class for a protocols that contains a id attribute
"""

from NetCatKS.DProtocol.api.implementors.actions import BaseProtocolActionsImplementor
from NetCatKS.DProtocol.api.interfaces.dymanic import IDynamicProtocolInterface

from zope.interface import implementer

__author__ = 'dimd'


@implementer(IDynamicProtocolInterface)
class DynamicProtocolImplementor(BaseProtocolActionsImplementor):

    """
    This class provides implementation of `session.interfaces.dynamic.IDynamicSessionInterface`
    Our public class have to inherit from here
    """

    def __init__(self, **kwargs):

        """

        :param kwargs:
        :return: void
        """

        self.__id = None
        super(DynamicProtocolImplementor, self).__init__(**kwargs)

    @property
    def id(self):

        """

        Return the protocol is
        :return: self__id

        """
        return self.__id

    @id.setter
    def id(self, _id):

        """

        Set the protocol id
        :param _id:
        :return: void

        """

        self.__id = _id
