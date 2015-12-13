"""
A Class representing our config loader, it providing a singleton pattern and methods that retrieve
a parts of our config represented as DynamicProtocol Object
"""

import json

from NetCatKS.Config.api.interfaces import IConfig
from NetCatKS.Config.api.implementers.configuration import TCP, WS, WEB, WAMP

from zope.interface import implementer
from zope.component import createObject


__author__ = 'dimd'


@implementer(IConfig)
class Config(object):

    """
    Trying to load config/config.json file and then load as JSON
    """

    __instance = None
    __config = None

    def __new__(cls):

        """

        Will trying to load our config file, by default will looking for a
        a config/config.json

        :return: void

        """
        if Config.__instance is None:

            Config.__instance = object.__new__(cls)

            try:

                with open('config/config.json', 'r') as config:
                    Config.__config = json.loads(config.read(), encoding='utf-8')

            except Exception as e_load:
                raise Exception('Config not found: {}'.format(e_load.message))

            else:

                config.close()

        return Config.__instance

    def __init__(self):
        pass

    @classmethod
    def get_section(cls, section):

        """
        Implementation of IConfig.get_section

        :param section:
        :type section: str

        :return: DynamicProtocol for this section if exist in our config - otherwise False

        """

        if section:

            proto = createObject(section)

            if section.upper() in cls.__config:
                return proto.to_object(cls.__config.get(section.upper()))

        else:
            return False

    @classmethod
    def get_tcp(cls):

        """
        Implementation of IConfig.get_tcp

        :return: DynamicProtocol
        """

        return cls.get_section('tcp')

    @classmethod
    def get_web(cls):

        """
        Implementation of IConfig.get_web

        :return: DynamicProtocol
        """

        return cls.get_section('web')

    @classmethod
    def get_wamp(cls):

        """
        Implementation of IConfig.get_wamp

        :return: DynamicProtocol
        """

        return cls.get_section('wamp')

    @classmethod
    def get_ws(cls):

        """
        Implementation of IConfig.get_ws

        :return: DynamicProtocol
        """

        return cls.get_section('ws')


__all__ = [
    'Config',
    'TCP',
    'WS',
    'WAMP',
    'WEB'
]
