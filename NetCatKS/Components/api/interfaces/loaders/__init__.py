"""
A module that contains interfaces about our internal and user defined loaders
"""
from zope.interface import Interface

__author__ = 'dimd'


class IBaseLoader(Interface):

    """
    An interface that describing our main loader
    """

    def load():

        """
        have to load the proper objects based on Interface filtering
        :return: list
        """


class IUserFactory(Interface):
    """
    Marker for user Factories
    """


class IUserStorage(Interface):
    """
    Marker for user Storages
    """


class IUserWampComponent(Interface):
    """
    marker for user defined wamp component, usually the implementer have to inherit
    from BaseWampComponent
    """


class IUserGlobalSubscriber(Interface):
    """

    The user Implementation of IUserGlobalSubscriber have to adpatee this interface.
    the user have to implement a factory that provide IUserGlobalSubscriber,
    the IUserGlobalSubscriber subscribe method will fire as actual global subscriber
    callback. The factory also have to adaptee IGlobalSubscribeMessage

    """
    def subscribe():
        """
        When we got something for our global subscriber this method will be fired
        :return:
        """


class IJSONResource(Interface):

    """
    Marker for JSON Resource.

    """
