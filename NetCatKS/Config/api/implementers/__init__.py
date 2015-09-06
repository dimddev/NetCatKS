__author__ = 'dimd'

import json

from NetCatKS.Config.api.interfaces import IConfig

from zope.interface import implementer


@implementer(IConfig)
class Config(object):
    """
    Trying to load config/config.py file and then load as JSON
    """
    __instance = None

    def __new__(cls):

        if Config.__instance is None:

            Config.__instance = object.__new__(cls)

        return Config.__instance

    def __init__(self):

        try:

            with open('config/config.json', 'r') as config:

                self.__config = json.loads(config.read(), encoding='utf-8')

            config.close()

        except Exception as e:
            raise Exception('Config not found: {}'.format(e.message))

        else:
            pass

    def get(self, section):
        return self.__config.get(section, None)