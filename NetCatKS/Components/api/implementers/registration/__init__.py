__author__ = 'dimd'

from ...interfaces.virtual import IVirtualAdapter
from ...interfaces.registration.adapters import IRegisterAdapters
from ...interfaces.registration.factories import IRegisterFactory

from ...implementers.default import DefaultAdapter
from ...implementers.registration.adapters import RegisterAdapter, FileAdaptersLoader
from ...implementers.registration.factories import RegisterFactory, FileFactoryLoader
from ...implementers.registration.session import SessionRegister, FileSessionsLoader

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
        sessions_source = kwargs.get('sessions_source', 'components/sessions')
        utility_source = kwargs.get('utility_source', 'components/utility')

        factories_prefix = kwargs.get('factories_prefix', 'Factory')
        adapters_prefix = kwargs.get('adapters_prefix', 'Adapter')
        sessions_prefix = kwargs.get('sessions_prefix', 'Protocol')

        if factories_source:

            self.__factory = RegisterFactory(
                FileFactoryLoader(factory_prefix=factories_prefix),
                factories_source
            )

            self.__factory.register_factories()

        if adapters_source:

            self.__radapter = RegisterAdapter(
                FileAdaptersLoader(factory_prefix=adapters_prefix),
                adapters_source,
                factory_prefix=adapters_prefix
            )

            self.__radapter.register_adapters()

        if sessions_source:

            self.__session = SessionRegister(
                FileSessionsLoader(factory_prefix=sessions_prefix),
                sessions_source
            )

            self.__session.register_sessions()

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