__author__ = 'dimd'

import imp
import os

from zope.interface import implementer
from zope.component import createObject

from NetCatKS.Components.api.interfaces import IBaseLoader


@implementer(IBaseLoader)
class BaseLoader(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.prefix = kwargs.get('factory_prefix', 'Factory')
        self.__storage = createObject('storageregister')

    def load(self, factories_source):

        """

        :param factories_source:
        :return:
        """

        __klasses = []
        __ignore = ['DefaultAdapter']

        for root, subdirs, files in os.walk(factories_source):

            if files:

                for f in files:

                    if f.endswith('.pyc'):
                        continue

                    mod_path = root.replace('/', '.')

                    load = imp.load_source(mod_path, root + '/' + f)

                    for klass in dir(load):

                        if klass.startswith('I'):

                            if klass in __klasses or klass == 'Interface':
                                continue

                            self.__storage.interfaces[getattr(load, klass).__name__.lower()] = {
                                'interface': getattr(load, klass),
                                'origin_name': getattr(load, klass).__name__
                            }

                        elif klass.endswith(self.prefix) and klass not in __ignore:
                            __klasses.append(getattr(load, klass))


        return __klasses
