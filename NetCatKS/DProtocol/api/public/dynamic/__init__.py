"""
A Public API for a Dynamic Protocol
"""

from NetCatKS.DProtocol.api.implementors.dynamic import DynamicProtocolImplementor

__author__ = 'dimd'


class DynamicProtocol(DynamicProtocolImplementor):

    """
    A Public API for a Dynamic Protocol
    """

    def __init__(self, **kwargs):

        """
        Will call the super constructor and will trying to verify the storage as valid

        :param kwargs:
        :return:

        """

        super(DynamicProtocol, self).__init__(**kwargs)

