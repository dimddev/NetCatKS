"""
A module that register user protocols as factories and if the they are register as subscribers,
will be created and dynamic subscriber tor it as well
"""
from NetCatKS.Components.api.interfaces.registration.protocols import IRegisterProtocols
from NetCatKS.Components.api.implementers.registration.factories import RegisterFactories
from NetCatKS.Components.api.interfaces import IJSONResource
from NetCatKS.Components.common.factory import RegisterAsFactory

from zope.interface import implementer

__author__ = 'dimd'


@implementer(IRegisterProtocols)
class RegisterProtocols(RegisterFactories):
    """
    We having use RegisterFactories as our base class, so all the jobs is done there
    """

    def __init__(self, protocols_source, file_loader=None, out_filter=None):

        """
        Will call our super and will take all actions to it

        :param protocols_source:
        :param file_loader:
        :param out_filter:

        :return: void
        """
        if not out_filter:
            out_filter = []

        default_filters = list(set(out_filter + [IJSONResource]))
        super(RegisterProtocols, self).__init__(protocols_source, file_loader, default_filters)

RegisterAsFactory(RegisterProtocols).register()
