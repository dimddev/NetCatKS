__author__ = 'dimd'

from NetCatKS.Components.api.implementers.default import DefaultAdapter
from NetCatKS.Components.api.interfaces.adapters import IDynamicAdapterFactory

from zope.component import adapter, createObject
from zope.component import getGlobalSiteManager
from zope.interface import implementer


class WampSessionProvider(object):

    def get_session(self):

        return createObject('storageregister').components.get(
            '__wamp_session__', False
        )

@implementer(IDynamicAdapterFactory)
class DynamicAdapterFactory(object):

    def __init__(self, *args, **kwargs):

        super(DynamicAdapterFactory, self).__init__()

        args = args[0]

        klass = adapter(*args)

        self.__klass = klass(
            type(
                kwargs.get('name', 'DynamicAdapter'),
                (DefaultAdapter, ),
                {}
            )
        )

        gsm = getGlobalSiteManager()
        gsm.registerAdapter(self.__klass)

    def get(self):
        return self.__klass