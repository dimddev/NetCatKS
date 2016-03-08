"""
A module providing a functionality for an incoming requests
"""

from zope.interface import implementer
from NetCatKS.Validators.api.interfaces.message import IMessage


__author__ = 'dimd'


@implementer(IMessage)
class Message(object):

    """
    A class represents an incoming message
    """

    def __init__(self, message):
        """
        A constructor
        :param message:
        :return:
        """
        self.message = message
