__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactory

from NetCatKS.Components.api.implementers.default import DefaultAdapter
from NetCatKS.Components.api.implementers.registration.adapters import RegisterAdapter, FileAdaptersLoader
from NetCatKS.Components.api.implementers.registration.factories import RegisterFactory, FileFactoryLoader
from NetCatKS.Components.api.implementers.registration.protocols import ProtocolRegister, FileProtocolsLoader
from NetCatKS.Components.api.implementers.registration.wamp import WampRegister, FileWampLoader

from zope.component import adapts
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter


class ComponentsRegistratorAdapter(DefaultAdapter):
    """
    Adapt together RegisterFactory and RegisterAdapters
    """
    adapts(IRegisterFactory, IRegisterAdapters)

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: adapters_source, factories_source, sessions_source, utility_source
        :return:
        """

        super(ComponentsRegistratorAdapter, self).__init__(*args)

        adapters_source = kwargs.get('adapters_source', 'components/adapters')
        factories_source = kwargs.get('factories_source', 'components/factories')
        protocol_source = kwargs.get('protocol_source', 'components/protocols')
        utility_source = kwargs.get('utility_source', 'components/utility')
        validators_source = kwargs.get('validators_source', 'components/validators')
        wamp_source = kwargs.get('wamp_source', 'components/wamp')

        if factories_source:

            self.__factory = RegisterFactory(
                FileFactoryLoader(),
                factories_source
            )

            self.__factory.register_factories()

        if adapters_source:

            self.__radapter = RegisterAdapter(
                FileAdaptersLoader(),
                adapters_source
            )

            self.__radapter.register_adapters()

        if protocol_source:

            self.__proto = ProtocolRegister(
                FileProtocolsLoader(),
                protocol_source
            )

            self.__proto.register_protocols()

        if wamp_source:

            self.__wamp = WampRegister(
                FileWampLoader(),
                wamp_source
            )

            self.__wamp.register_wamp()

    def init(self):
        """

        :return:
        """
        return getMultiAdapter(
            [self.__factory, self.__radapter],
            IVirtualAdapter
        )


class ComponentsRegistration(ComponentsRegistratorAdapter):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        super(ComponentsRegistration, self).__init__(*args, **kwargs)


gsm = getGlobalSiteManager()
gsm.registerAdapter(ComponentsRegistration)


__all__ = [
    'ComponentsRegistration',
    'ComponentsRegistratorAdapter'
]