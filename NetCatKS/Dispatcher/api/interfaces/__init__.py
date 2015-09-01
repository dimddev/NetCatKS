__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IJSONResource(Interface):

    """
    JSON Resource. This interface have to provide two attributes, used for implementer.

    The `adapter` is our first argument in the constructor. It's used from the adapter pattern
    and have to be from type IValidatorResponse

    The `protocol` attribute is designed to be provided by classes which are subclasses our IJSONResource,
    implementer, usually is instance of our DynamicProtocol

    """

    adapter = Attribute("The implementer have to provie this attribute it's used by subscribers")
    protocol = Attribute("descrive be protocol")

    def compare():
        """
        Designed to copare the the adapter and the protocol signature
        if the signatures is equal
        """

class IXMLResource(Interface):
    """
    XML Resource marker
    """


class IHTMLResource(Interface):
    """
    HTML Resource marker
    """

