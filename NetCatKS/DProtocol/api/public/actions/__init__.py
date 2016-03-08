"""
A public API for a BaseProtocolActions
"""

from NetCatKS.DProtocol.api.implementors.actions import BaseProtocolActionsImplementor
__author__ = 'dimd'


class BaseProtocolActions(BaseProtocolActionsImplementor):

    """
    Most of the Dynamic Protocol implementers have to use this class as base
    """

    def __init__(self, **kwargs):

        """
        The Constructor, just call the super
        :param kwargs:
        :return: void

        """
        super(BaseProtocolActions, self).__init__(**kwargs)
