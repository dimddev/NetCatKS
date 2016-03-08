"""
A module interface that contains a validator interfaces
"""

from zope.interface import Interface, Attribute

__author__ = 'dimd'


class IValidator(Interface):

    """
    An interface for a default validation
    """
    is_valid = Attribute('is this message valid')
    message_type = Attribute('show us the type of the message')

    def validate():
        """
        Validate incoming message for our supported types
        :return: self
        """


class IValidatorResponse(Interface):
    """
    An interface for a default response validation
    """
    response = Attribute(
        """
        Helper interface that provides attribute to hold a valid response from our main validator
        """
    )
