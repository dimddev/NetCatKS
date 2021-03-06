"""
A module that providing a default validation functionality
"""

from zope.component import adapts
from zope.interface import implementer

from NetCatKS.Validators.api.interfaces.validators import IValidator
from NetCatKS.Validators.api.interfaces.message import IMessage


__author__ = 'dimd'


@implementer(IValidator)
class BaseValidator(object):

    """
    The BaseValidator class provides our initial data for all validators and adapt IMessage interface, which
    comes with message attribute. The validate method have to be implemented
    """
    adapts(IMessage)

    def __init__(self, validate_msg):

        """
        Our constructor will setup is_valid to False, message_type and message to None
        :param validate_msg: can be anything: json, binary etc..
        """

        super(BaseValidator, self).__init__()

        self.validate_msg = validate_msg

        self.is_valid = False
        self.message_type = None
        self.message = None

    def validate(self):

        """
        Method wich have to validate some data type

        :return: self
        """
        raise NotImplementedError('Not implemented, must be sub classed')
