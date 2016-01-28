"""
A module interface for incoming request
"""

from zope.interface import Interface, Attribute

__author__ = 'dimd'


class IMessage(Interface):
    """
    Interface which provide a message attribute, representing incoming message.
    The message usually is the data who arrived to us from some where
    """
    message = Attribute("Represent incoming message")
