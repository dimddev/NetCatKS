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

    The implementer have to keep the schema like so:

    1. the request:

        {"command": "event", "id": 42, "clock": 1441461133.176596}

    2. Make API that have a mirror attributes for mapping
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

    IBaseResourceSubscriber provides functionality for comparison of the signature on
    a incoming request against a candidate DProtocol implementation registered as
    IJSONResource

    The `adapter` is our first argument in the constructor. It's used from the adapter pattern
    and have to be from type IJSONResource

    The `protocol` attribute is designed to be provided by classes which are implements IJSONResourceSubscriber,
    or inherit from DProtocolSubscriber. If subclass does not provide the protocol argument will
    raise AttributeError.

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