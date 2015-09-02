__author__ = 'dimd'

import json

from ..default import BaseValidator
from NetCatKS.Logger import Logger

from zope.component import getGlobalSiteManager


class JSONValidator(BaseValidator):
    """
    This class provide functionality for validating whether incoming data is JSON
    """

    def __init__(self, validate_msg):
        """

        :param validate_msg: IValidatorResponse
        :return:
        """
        super(JSONValidator, self).__init__(validate_msg)

        self.__logger = Logger()

    def validate(self):

        try:
            __json = json.loads(self.validate_msg.message)

        except Exception as e:

            self.__logger.error('JSON Validator error: {}'.format(e.message))

            self.is_valid = False
            self.message_type = 'JSON'
            self.message = self.validate_msg.message

            return self

        else:

            self.is_valid = True
            self.message_type = 'JSON'
            self.message = __json

            return self

gsm = getGlobalSiteManager()
gsm.registerSubscriptionAdapter(JSONValidator)