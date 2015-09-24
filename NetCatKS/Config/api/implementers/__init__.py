__author__ = 'dimd'

import json

from NetCatKS.Config.api.interfaces import IConfig
from NetCatKS.Config.api.implementers.configuration import *

from zope.interface import implementer
from zope.component import createObject


@implementer(IConfig)
class Config(object):
    """
    Trying to load config/config.json file and then load as JSON
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

        except Exception as e:
            raise Exception('Config not found: {}'.format(e.message))

        else:

            config.close()

            __all = {}

            tcp = createObject('tcp').to_dict()
            __all['tcp'] = tcp

            web = createObject('web').to_dict()
            __all['web'] = web

            wamp = createObject('wamp').to_dict()
            __all['wamp'] = wamp

            # print json.dumps(__all, indent=4)

    def get(self, section):
        return self.__config.get(section, None)


__all__ = [
    'Config'
]
