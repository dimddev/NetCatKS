"""
A Public API for a Protocol Filters
"""
from NetCatKS.DProtocol.api.implementors.filters import ProtocolFiltersImplementor

__author__ = 'dimd'


class ProtocolFilters(ProtocolFiltersImplementor):

    """
    Can be used as independent filtering
    """

    def __init__(self):

        """
        Constructor, just calling a super
        :return: void
        """

        super(ProtocolFilters, self).__init__()
