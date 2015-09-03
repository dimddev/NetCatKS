__author__ = 'dimd'

from ...interfaces.validators import IValidator
from ...implementers.message import Message

from default import BaseValidator, ValidatorResponse
from html import HTMLValidator
from json import JSONValidator
from xml import XMLValidator

from NetCatKS.Logger import Logger

from zope.component import subscribers
from zope.interface import implementer


@implementer(IValidator)
class Validator(BaseValidator):

    """
    Our main validator will trying to resolve the type of incoming request
    """

    def __init__(self, validate_msg):
        """
        Accept message that have to be validated

        :param validate_msg: currently we support json, xml and html validators
        """
        super(Validator, self).__init__(validate_msg)

        self.__msg = Message(validate_msg)
        self.__logger = Logger()

    def validate(self):

        """
        Will walk through all subscribers from IValidator type
        the first one will be returned as valid type. In this way we can supporting a lot of types
        on the same port/service

        :return: matched IValidator subscriber
        """
        for sub in subscribers([self.__msg], IValidator):

            msg = sub.validate()

            self.is_valid = msg.is_valid
            self.message_type = msg.message_type
            self.message = msg.message

            # we want only one correct type of our message so
            # only one validator will response with True

            if self.is_valid is True:

                self.__logger.info('Matched type is: {}'.format(self.message_type))

                return self
        else:

            self.__logger.info('There are no subscribers from type IValidator')

            return False

__all__ = [
    'Validator',
    'ValidatorResponse',
    'BaseValidator',
    'HTMLValidator',
    'JSONValidator',
    'XMLValidator'
]