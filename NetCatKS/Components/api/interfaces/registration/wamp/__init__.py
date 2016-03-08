"""
A good place for interfaces related for a wamp components
"""

from zope.interface import Interface, Attribute
__author__ = 'dimd'


class IRegisterWamp(Interface):

    """
    Base interface for a RegisterWamp implementation
    """

    def register():
        """
        Registering of all objects which belong to IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent
        :return: void
        """


class IWAMPResource(Interface):
    """
    marker
    """


class IWAMPComponent(Interface):

    """
    A Interface that is for internal usage and its implementation will be a helper class
    for a easy creating of wamp components
    """

    def set_session(session):
        """
        register session to self.session
        :param session: Wamp Session
        :return:
        """


class IWAMPLoadOnRunTime(Interface):
    """
    marker for API's that have to be run, after we join in WAMP session
    """

    def load():
        """
        trying to load on runtime some wamp RPC
        :return: IJSONResource
        """
