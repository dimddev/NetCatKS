"""
A common module used for all object loading operations
"""

import imp
import os

from zope.interface import implementer
from zope.component import createObject
from zope.interface import implementedBy

from NetCatKS.Components.api.interfaces import IBaseLoader

__author__ = 'dimd'


@implementer(IBaseLoader)
class BaseLoader(object):

    """
    Will walk through our component directory and will try to load all matched object described
    as interfaces
    """

    def __init__(self):
        """
        Load the storage
        :param kwargs:
        :return:
        """
        self.__storage = createObject('storageregister')

    @staticmethod
    def is_register(obj, filter_interfaces):
        """
        Will check whether the object is register or not

        :param obj:

        :param filter_interfaces:
        :return: tuple
        """
        try:

            is_reg = [
                (obj, candidate) for candidate in filter_interfaces if candidate in implementedBy(obj)
            ][-1]

        except IndexError:
            return False

        else:
            return is_reg

    def __filtering(self, load, filter_interface):

        """
        Loop through loaded object and if is registered will be append to our list

        :param load:

        :param filter_interface:

        :return: list
        """

        __klasses = []
        __ignore = ['DefaultAdapter']

        for klass in dir(load):

            try:

                klass_obj = getattr(load, klass)
                candidate = self.is_register(klass_obj, filter_interface)

            except TypeError:
                pass

            else:

                if candidate and klass not in __ignore:
                    __klasses.append(candidate)

        return __klasses

    def load(self, factories_source, filter_interface):

        """
        Load objects recursively

        :param factories_source:
        :type factories_source: str

        :param filter_interface:
        :type filter_interface: list

        :return: loaded classes
        """

        __klasses = []

        for root, _, files in os.walk(factories_source):

            if files:

                for f in files:

                    if f.endswith('.pyc'):
                        continue

                    mod_path = root.replace('/', '.')

                    load = imp.load_source(mod_path, root + '/' + f)
                    __klasses = self.__filtering(load, filter_interface)

        return __klasses
