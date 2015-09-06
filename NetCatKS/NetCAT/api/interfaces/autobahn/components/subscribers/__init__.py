__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IGlobalSubscriberCallback(Interface):

    """

    The user Implementation of IUserGlobalSubscriber hato to adpatee this interface.
    the user have to implement a factory that provide IUserGlobalSubscriber,
    the IUserGlobalSubscriber subscribe method will fire as actual global subscriber
    callback. The factory also have to adaptee IGlobalSubscribeMessage

    """
    def subscribe():
        """

        :return:
        """