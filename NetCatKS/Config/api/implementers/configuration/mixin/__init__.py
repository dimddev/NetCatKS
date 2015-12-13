"""
This module is written in a DynamicProtocol style and caring for our Mixin configuration
"""
from __future__ import absolute_import

from zope.interface import Interface, Attribute, implementer
from zope.component import getGlobalSiteManager

from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions


__author__ = 'dimd'


class MixinConfiguration(object):
    """
    A mixin configuration for a TCP and WEB servers
    """
    pass


class RegisterAsFactory(object):

    """
    A class that providing a shortcut for a register a class as Zope Factory
    This mechanism is a important for us because we having loaded all user defined callbacks and protocols
    on runtime, this including our internal configuration too
    """

    def __init__(self, klass):

        """

        The constructor will care about the class that have to be register as Factory
        :param klass:
        :type klass: class

        :return: void
        """

        self.__gsm = getGlobalSiteManager()
        self.__klass = klass

    def register(self):

        """
        Registering a class as Zope Factory, you can load this factory with a createObject

        :return: void
        """

        self.__gsm.registerUtility(
            Factory(self.__klass, self.__klass.__name__),
            IFactory,
            self.__klass.__name__.lower()
        )
