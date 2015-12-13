"""
This module is written in a DynamicProtocol style and caring for our WAMP client (component)
"""
from zope.interface import implementer
from NetCatKS.Config.api.implementers.configuration.mixin import RegisterAsFactory
from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.interfaces import IWamp

__author__ = 'dimd'


@implementer(IWamp)
class WAMP(BaseProtocolActions):

    """
    An implementation of IWamp
    """

    def __init__(self):

        """
        In the constructor we providing a default for all properties

        :return: void
        """
        self.__user = 'wamp_cra_username'
        self.__password = 'wamp_cra_password'
        self.__service_name = 'wamp service name'
        self.__url = 'ws://localhost:8080/ws'
        self.__realm = 'realm1'
        self.__port = 8080
        self.__protocol = 'ws'
        self.__retry_interval = 2
        self.__path = 'ws'
        self.__hostname = 'localhost'

    @property
    def user(self):
        """
        A getter for a wamp cra user
        :return: str
        """
        return self.__user

    @user.setter
    def user(self, user):

        """

        A setter for wamp cra user
        :param user:
        :type user: str

        :return: void
        """

        self.__user = user

    @property
    def password(self):

        """
        A getter for a wamp cra password

        :return: str
        """
        return self.__password

    @password.setter
    def password(self, password):

        """
        A setter for a wamp cra password
        :param password:
        :type password: str

        :return: void
        """
        self.__password = password

    @property
    def service_name(self):

        """
        A setter for our wamp servise name

        :return: str
        """
        return self.__service_name

    @service_name.setter
    def service_name(self, name):

        """
        A getter for our wamp servise name
        :param name:
        :type name: str

        :return: void
        """
        self.__service_name = name

    @property
    def url(self):

        """
        A getter for our wamp url
        :return: str
        """

        return self.__url

    @url.setter
    def url(self, url):

        """
        A setter for our wamp url
        :param url:
        :type url: str

        :return: void
        """
        self.__url = url

    @property
    def realm(self):
        """
        A getter for our wamp realm
        :return: str
        """
        return self.__realm

    @realm.setter
    def realm(self, realm):

        """
        A setter for our wamp realm
        :param realm:
        :type realm: str

        :return: void
        """
        self.__realm = realm

    @property
    def port(self):

        """
        A getter for our wamp port

        :return: int
        """
        return self.__port

    @port.setter
    def port(self, port):

        """
        A setter for our wamp port
        :param port:
        :type port: int

        :return: void
        """
        self.__port = port

    @property
    def protocol(self):

        """
        A setter for our wamp protocol

        :return: str
        """

        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):

        """
        A setter for our wamp protocol
        :param protocol:
        :type protocol: str

        :return:
        """

        self.__protocol = protocol

    @property
    def retry_interval(self):

        """
        A getter for our wamp connection retry interval in second

        :return: int
        """

        return self.__retry_interval

    @retry_interval.setter
    def retry_interval(self, interval):

        """
        A setter for our wamp connection retry interval in second
        :param interval:
        :type interval: int

        :return: void
        """

        self.__retry_interval = interval

    @property
    def path(self):
        """
        A getter for a Wamp Web Socket path

        :return: str
        """

        return self.__path

    @path.setter
    def path(self, path):

        """
        A setter for our wamp ws path
        :param path:
        :type path: str

        :return: void
        """

        self.__path = path

    @property
    def hostname(self):

        """
        A getter for our wamp hostname

        :return: str
        """

        return self.__hostname

    @hostname.setter
    def hostname(self, host):

        """
        A setter for our wamp hostname
        :param host:
        :type host: str

        :return: void
        """
        self.__hostname = host

RegisterAsFactory(WAMP).register()
