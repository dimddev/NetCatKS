__author__ = 'dimd'

from zope.interface import implementer
from zope.component import adapts, subscribers
from zope.component import getGlobalSiteManager

from NetCatKS.Dispatcher.api.public import  IDispatcher, IJSONResource
from NetCatKS.Validators.api.public import IValidator, ValidatorResponse
from NetCatKS.Logger import Logger


@implementer(IDispatcher)
class Dispatcher(object):
    """
    Our Main dispatcher, Will trying to dispatch the request to API which provides functionality for it.
    The Dispatcher also adapts IValidator
    """
    adapts(IValidator)

    def __init__(self, validator):
        self.validator = validator
        self.__logger = Logger()

    def dispatch(self):
        """
        When request is happening first will be validated,
        if valid_dispatch is False means we do not support this data type. You have to write your custom
        validator(s) inside components/validators
        Otherwise
        :return:
        """
        valid_dispatch = self.validator.validate()

        if valid_dispatch is False:
            return self.validator

        result = ValidatorResponse(valid_dispatch.message)

        if valid_dispatch.message_type == 'JSON':

            for sub in subscribers([result], IJSONResource):

                self.__logger.info('Matched subscribers: {}'.format(sub))

                comp = sub.compare()

                if comp is not False:

                    self.__logger.info('Signature compare to {}'.format(comp))

                    return comp

            else:

                self.__logger.warning('There are no API subscribers for type: {}'.format(
                    valid_dispatch.message_type
                ))

                return False

gsm = getGlobalSiteManager()
gsm.registerAdapter(Dispatcher)