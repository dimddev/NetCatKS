"""
This module is written in a DynamicProtocol style and caring for our WAMP client (component)
"""
from zope.interface import implementer
from NetCatKS.Config.api.implementers.configuration.mixin import RegisterAsFactory
from NetCatKS.Config.api.interfaces import IWamp
from NetCatKS.Config.api.implementers.configuration.mixin import MixinSharedConfig, MixinWamp
__author__ = 'dimd'


@implementer(IWamp)
class WAMP(MixinSharedConfig, MixinWamp):

    """
    An implementation of IWamp
    """

    def __init__(self):

        """
        In the constructor we providing a default for all properties

        :return: void
        """

        super(WAMP, self).__init__()

        self.__user = 'wamp_cra_username'
        self.__password = 'wamp_cra_password'
        self.__realm = 'realm1'
        self.__retry_interval = 2
        self.__path = 'ws'
        self.url = 'ws://localhost:8080'
        self.port = 8080

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


RegisterAsFactory(WAMP).register()
