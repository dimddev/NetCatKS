__author__ = 'dimd'

from ...interfaces.validators import IValidator
from ...implementers.message import Message

from default import BaseValidator, ValidatorResponse
from html import HTMLValidator
from json import JSONValidator
from xml import XMLValidator

from zope.component import subscribers
from zope.interface import implementer



@implementer(IValidator)
class Validator(BaseValidator):

    def __init__(self, validate_msg):

        super(Validator, self).__init__(validate_msg)

        self.__msg = Message(validate_msg)

    def validate(self):

        for sub in subscribers([self.__msg], IValidator):

            msg = sub.validate()

            self.is_valid = msg.is_valid
            self.message_type = msg.message_type
            self.message = msg.message

            # we want only one correct type of our message so
            # only one validator will response with True

            if self.is_valid is True:
                return self

        return False

__all__ = [
    'Validator',
    'ValidatorResponse',
    'BaseValidator',
    'HTMLValidator',
    'JSONValidator',
    'XMLValidator'
]