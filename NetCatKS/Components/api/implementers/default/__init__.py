"""
A module contains a base class for all dynamic adapters
"""

from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter
from NetCatKS.Components.common.adapters import AdapterProxyGetter

from zope.interface import implementer

__author__ = 'dimd'


@implementer(IVirtualAdapter)
class DefaultAdapter(AdapterProxyGetter):

    """
    A base class for all dynamic adapters
    """

    def __init__(self, *args):

        """
        Just calling a super

        :param args:

        :return: void
        """
        super(DefaultAdapter, self).__init__(*args)
