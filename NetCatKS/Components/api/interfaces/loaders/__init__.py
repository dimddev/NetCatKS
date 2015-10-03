__author__ = 'dimd'

from zope.interface import Interface


class IBaseLoader(Interface):

    def load(self):
        """

        :return:
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

        :return:
        """


class IJSONResourceRootAPI(Interface):

    """
    Marker for API's which adapts IJSONResource

    All API's from this type have to be stored inside components/adapters
    directory. They will be loaded on runtime by NetCatKS and will be registered
    as SubscriptionAdapter inside zope global site manager.

    Later, when request arriving the Dispatcher will deal with all adapter API's which are registered
    as IJSONResourceRootAPI implementer

    The implementer of this interface have to provide a functionality
    that deal with structures defined by DProtocol API. By default all
    of them is expected to by from type IJSONResource.

    The implementer have to use zope.interface.implementer to mark
    an API as resource from type IJSONResourceAPI and zope.compoment.adapts
    for an adapting an IJSONResource

    The API from type IJSONResourceAPI must provide functionality that deals
    with root based structures, which meaning we have one root element and
    inside it our custom structures or:

    {"time_operation":
        {
            "location" : {
                "longitude": 34.342424,
                "latitude": 12.333456
            },
            "user_id": 1
        }
    }

    or

    {"user_data":
        {
            "user_id": 1
        }
    }

    or even

    {"time": 1232131231}

    so when we got one element inside our JSON request NetCatKS internally will looking
    for API's from a type IJSONResourceAPI and all of them have to implement process_factory
    method, it will be called as callback when we got a request.

    How the API will recognize which API to call?

    Here we talking for a API called root API, and NetCatKS will looking for API name that
    response on the our root element name or:

    @implementer(IJSONResourceAPI):
    class MyTestAPI(object):

        adapts(IJSONResource)

        def __init__(self, factory_json):
            self.factory = factory_json

        def process_factory(self):

            print self.factory.to_dict()
            # here we dealing with our request for the fist time

            # and we have to return IJSONResource implementation
            # we also can define additional DProtocol structures
            # that can be used here, for our response instead self.factory

            return self.factory


    will trigger on a request with structure like {"mytestapi": ""}
    and all the data from the request will be passed to our API constructor
    as first argument. Then  NetCatKS will call process_factory, the place when
    you have to deal with this data.

    @implementer(IJSONResourceAPI)
    class Convert(object):

        adapts(IJSONResource)

        def __init__(self, factory_json):
            self.factory = factory

        def process_factory(self):

            self.factory.convert.id = 4200
            return self.factory

    as above one but will trigger on {"convert": ""}

    If the service that require this API is a TCP or a WEB the result
    will be returned to the client immediately, but if the service is a WAMP
    the result will be redirected to our global subscriber from where you have
    possibility to publish this data to another subscribers.

    All API's which are registered under this interface have to be registered as
    subscriber adapters and will fire when protocol from DProtocol type or other
    IJSONResource comes as request.
    """

    def process_factory():
        """

        :return: IJSONResource
        """