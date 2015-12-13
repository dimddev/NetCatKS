"""
A module that contain interface which represents our Config object
"""

from zope.interface import Interface
from NetCatKS.Config.api.interfaces.confguration import *

__author__ = 'dimd'


class IConfig(Interface):

    """
    Interface IConfig
    """

    def get_section(section):

        """
        The main getter for all the others, will get the requested section from a loaded
        config file, where the section is represented as uppercase string

        :param section:
        :type section: str

        :return: DynamicProtocol for this section if exist in our config - otherwise False

        """

    def get_tcp():

        """
        Will retrieve a tcp section from a config file
        :return: DynamicProtocol
        """

    def get_web():

        """
        Will retrieve a web section from a config file
        :return: DynamicProtocol
        """

    def get_wamp():

        """
        Will retrieve a wamp section from a config file
        :return: DynamicProtocol
        """

    def get_ws():

        """
        Will retrieve a web socket section from a config file
        :return: DynamicProtocol
        """
