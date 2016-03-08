"""
A module that provide a base functionality for loading files and all objects inside it
on run time. All loaded object will be filtering by interfaces
"""
from __future__ import absolute_import
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
    A base class used from all loaders
    """
    def __init__(self):
        """

        :param kwargs:
        :return:
        """
        self.__storage = createObject('storageregister')

    @staticmethod
    def is_register(obj, filter_interfaces):
        """
        Will trying to match object to its interface implementation
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

    def __filter(self, klasses, load, filter_interface, ignore):
        """
        A object filtering base on filter interface and ignore list
        :param klasses:
        :param load:
        :param filter_interface:
        :param ignore:
        :return:
        """
        for klass in dir(load):

            try:

                klass_obj = getattr(load, klass)
                candidate = self.is_register(klass_obj, filter_interface)

            except TypeError:
                pass

            else:

                if candidate and klass not in ignore:
                    klasses.append(candidate)

        return klasses

    def load(self, factories_source, filter_interface):

        """
        Load a modules

        :param factories_source:
        :type factories_source: str

        :param filter_interface:
        :type filter_interface: list

        :return:
        """

        __klasses = []
        __ignore = ['DefaultAdapter']

        for root, _, files in os.walk(factories_source):

            if files:

                for f in files:

                    if f.endswith('.pyc'):
                        continue

                    mod_path = root.replace('/', '.')

                    load = imp.load_source(mod_path, root + '/' + f)

                    __klasses = self.__filter(
                        __klasses, load, filter_interface, __ignore
                    )

        return __klasses
