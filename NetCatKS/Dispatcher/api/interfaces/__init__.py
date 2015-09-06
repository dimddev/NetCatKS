__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IHTMLResource(Interface):
    """
    HTML Resource marker
    """


class IHTMLResourceAPI(Interface):
    """
    marker for API's which support IHTMLResource
    """


class IHTMLResourceSubscriber(Interface):
    """

    """


class IJSONResource(Interface):

    """
    Marker for JSON Resource.

    """


class IJSONResourceAPI(Interface):

    """
    Marker for API's which support IJSONResource

    API's that have to be implemented for a users
    to deal with the requests from type IJSONResource

    When we have registered API from this type
    it will be executed internally inside our main Dispatcher,
    if the service that require this API is tcp or web the result
    will be returned to the client in a moment, but if the running service is wamp
    the result will be redirected to our global subscriber.

    All API's which are registered under this interface have to be registered as
    subscriber adapters and will fire when protocol from DProtocol type or other
    IJSONResource comes as request.

    The implementer have to keep the schema like so:

    1. the request:

        {"command": "event", "id": 42, "clock": 1441461133.176596}

    2. Then we have to make few things

    2.1. Make sure that we have DProtocol implementation of this request

    2.2. Mark your DProtocol as IJSONResource

    2.3. Implement IJSONResourceSubscriber

    2.4. Create API which implement IJSONResourceAPI

    2.4.1 Must adapt IJSONResource

    3. Make API that have a mirror attributes for mapping
    so if the request has key command with value event,
    we can write the IJSONResourceAPI implementation like this:

        @implementer(IJSONResourceAPI)
        class Command(object):

            adapts(IJSONResource)

            def __init__(self, adapter):
                self.adapter = adapter

            def event(self):
                # works here with self.adapter
    """


class IJSONResourceSubscriber(Interface):
    """

    """


class IBaseResourceSubscriber(Interface):

    """
    The subclass have to inherit from DProtocolSubscriber, which implements IJSONResourceSubscriber
    and adapts IJSONResource, all what we need

    The `adapter` is our first argument in the constructor. It's used from the adapter pattern
    and have to be from type IJSONResource

    The `protocol` attribute is designed to be provided by classes which are implements IJSONResourceSubscriber,
    or inherit from DProtocolSubscriber. If subclass does not provide the protocol argument will
    raise AttributeError.

    DProtocolSubscriber does not provides this attribute by default so, it must be declared by user

    """

    adapter = Attribute("The implementer have to provide implementation of IJSONResource")
    protocol = Attribute("DProtocol instance")

    def compare():
        """
        Designed to compare the the adapter and the DProtocol signature
        if the signatures is equal
        """


class IXMLResource(Interface):
    """
    XML Resource marker
    """


class IXMLResourceAPI(Interface):
    """
    marker for API's which support IXMLResource
    """


class IXMLResourceSubscriber(Interface):
    """

    """