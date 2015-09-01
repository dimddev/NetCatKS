__author__ = 'dimd'

from ....api.implementers.default import DefaultAdapter
from ...interfaces.adapters import IDynamicAdapterFactory

from zope.component import adapter
from zope.component import getGlobalSiteManager
from zope.interface import implementer


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