"""
A module that providing a public helpers for easy build of a "NetCatKS" applications
"""

from NetCatKS.Components.api.interfaces.adapters import IRequestSubscriber

from zope.component import createObject, adapts
from zope.interface import implementer

from NetCatKS.Components.api.interfaces.adapters import IJSONResourceRootAPI, IJSONResourceAPI
from NetCatKS.Components.api.interfaces.loaders import IJSONResource
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPLoadOnRunTime

__author__ = 'dimd'


class _WampSessionProvider(object):
    """
    Will try to provide a saved wamp session inside our storage
    if not success will return False
    """

    @staticmethod
    def get_session():

        """
        Trying to retrieve a wamp session from a storage

        :return: wamp session or False
        """

        return createObject('storageregister').components.get(
            '__wamp_session__', False
        )


@implementer(IJSONResourceAPI)
class BaseAPI(object):

    """
    A helper class, that have to be used from the user as base, when this is done
    the user implementation will be marked as as BaseAPI. Read more in IJSONResourceAPI docs
    """

    adapts(IJSONResource)

    def __init__(self, factory):

        """
        We have to initialize our factory object, it's represent a user defined API
        :param factory:

        :return: void
        """
        self.factory = factory


@implementer(IJSONResourceRootAPI)
class BaseRootAPI(object):

    """
    A helper class, that have to be used from the user as base, when this is done
    the user implementation will be marked as as BaseRootAPI. Read more in IJSONResourceRootAPI docs
    """

    adapts(IJSONResource)

    def __init__(self, factory):
        """
        We have to initialize our factory object, it's represent a user defined API
        :param factory:

        :return: void
        """
        self.factory = factory

    def process_factory(self):

        """
        Not Implemented. This method have to be implemented from a user when there are a api from BaseRootAPI type

        :return: void
        """
        raise NotImplementedError('You have to implement this method in your API')


class BaseAPIWampMixin(BaseAPI, _WampSessionProvider):

    """
    A mixin class that providing a BaseAPI with a "WAMP" support
    """

    def __init__(self, factory):

        """
        Just call a super
        :param factory:
        :type factory: user defined api from BaseAPIWampMixin type

        :return: void
        """
        super(BaseAPIWampMixin, self).__init__(factory)


class BaseRootAPIWampMixin(BaseRootAPI, _WampSessionProvider):

    """
    A mixin class that providing a BaseRootAPI with a "WAMP" support
    """

    def __init__(self, factory):

        """
        Just calling a super
        :param factory:
        :type factory: a user defined API

        :return: void
        """
        super(BaseRootAPIWampMixin, self).__init__(factory)

    def process_factory(self):

        """
        Not Implemented. This method have to be implemented from a user when there are a api from BaseRootAPI type

        :return: void
        """
        raise NotImplementedError('You have to implement this method in your API')


@implementer(IWAMPLoadOnRunTime)
class WAMPLoadOnRunTime(_WampSessionProvider):

    """
    Will be called when we are connected to crossbar router and onJoin occur
    so it's useful when we want to make a initial request from a wamp services
    """

    adapts(IJSONResource)

    def __init__(self, factory):

        """
        Just calling a super
        :param factory:
        :param factory: a user defined API

        :return: void
        """
        self.factory = factory

    def load(self):

        """
        Abstract method that have to be implemented by the user, This method will be used
        when onJoin occur

        :return: void
        """
        raise NotImplementedError('You have to implement this method in your API')


@implementer(IRequestSubscriber)
class RequestSubscriber(object):

    """
    A helper class that will mark a user defined protocol as subscriber, when request occur,
    this protocol will be listed as one of possible chosen
    """

    @staticmethod
    def subscribe_me():

        """
        Subscribe a protocol to listen for a request
        :return:
        """

        return True
