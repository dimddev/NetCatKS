__author__ = 'dimd'

from twisted.internet.defer import Deferred

from zope.interface import implementer
from zope.component import adapts, subscribers
from zope.component import getGlobalSiteManager
from zope.interface.verify import verifyObject

from NetCatKS.Dispatcher.api.public import IDispatcher, IJSONResourceSubscriber, IJSONResourceAPI, IJSONResource
from NetCatKS.Dispatcher.api.public import IXMLResourceSubscriber, IXMLResourceAPI, IXMLResource
from NetCatKS.Validators.api.public import IValidator, ValidatorResponse
from NetCatKS.Dispatcher.api.public import IDispathcherResultHelper
from NetCatKS.Logger import Logger


@implementer(IDispatcher)
class Dispatcher(object):

    """
    Our Main dispatcher, Will trying to dispatch the request to API which provides functionality for it.
    The Dispatcher also adapts IValidator
    """

    adapts(IValidator)

    def __init__(self, validator):
        """

        :param validator:
        :type:

        """
        self.validator = validator
        self.__logger = Logger()

    def __api_processor(self, valid_dispatch, valid_response, isubscriber, iapi, iresource):
        """

        :param valid_dispatch:
        :param valid_response:
        :param isubscriber:
        :param iapi:
        :param iresource:
        :return:
        """
        for sub in subscribers([valid_response], isubscriber):

            self.__logger.debug('Matched subscribers: {}'.format(sub.__class__.__name__))

            try:

                verifyObject(isubscriber, sub)

            except Exception as e:

                self.__logger.warning('Incorrect implementation: {}'.format(e))

            else:

                comp = sub.compare()

                if comp is not False and iresource.providedBy(comp):

                    self.__logger.debug('Signature compare to {}'.format(comp.__class__.__name__))

                    # trying to resolve API that will deal with these request

                    for api in subscribers([comp], iapi):

                        # process request without root element
                        if len(comp.to_dict().keys()) > 1:

                            if api.__class__.__name__.lower() in comp.to_dict().keys():

                                self.__logger.debug('Candidate API {} for {}'.format(
                                    api.__class__.__name__,
                                    comp.__class__.__name__
                                ))

                                candidate_api_name = comp.to_dict().get(api.__class__.__name__.lower())

                                try:
                                    # execute the candidate API method
                                    # and return the result
                                    candidate_api_result = getattr(api, candidate_api_name)()

                                except AttributeError as e:

                                    msg = 'Candidate API {} for {} does not implement method {} error: {}'

                                    self.__logger.warning(msg.format(
                                        api.__class__.__name__,
                                        comp.__class__.__name__,
                                        candidate_api_name,
                                        e.message
                                    ))

                                else:

                                    self.__logger.info('Successful apply API {} for {}'.format(
                                        api.__class__.__name__,
                                        comp.__class__.__name__
                                    ))

                                    return candidate_api_result
                        else:

                            # root element
                            #print api.__class__.__name__.lower() in comp.to_dict().keys()
                            if api.__class__.__name__.lower() in comp.to_dict().keys():

                                self.__logger.debug('Candidate API {} for {}'.format(
                                    api.__class__.__name__,
                                    comp.__class__.__name__
                                ))

                                self.__logger.info('Successful apply API {} for {}'.format(
                                    api.__class__.__name__,
                                    comp.__class__.__name__
                                ))

                                return api.process_factory()

        # if there are no one subsciber from IJSONResource

        self.__logger.warning('There are no API subscribers for type: {} subscriber: {}, API: {}, Resource: {}'.format(
            valid_dispatch.message_type, isubscriber.__name__, iapi.__name__, iresource.__name__
        ))

        return False

    def dispatch(self):
        """
        When request is happening first will be validated,
        if valid_dispatch is False means we do not support this data type. You have to write your custom
        validator(s) inside components/validators
        Otherwise

        :return:
        """
        # validate for supporting types

        try:
            valid_dispatch = self.validator.validate()

        except Exception as e:

            self.__logger.debug('validate error: {}'.format(e.message))
            return self.validator

        else:

            if valid_dispatch is False:
                return self.validator

            valid_response = ValidatorResponse(valid_dispatch.message)

            if valid_dispatch.message_type == 'JSON':

                return self.__api_processor(
                    valid_dispatch,
                    valid_response,
                    IJSONResourceSubscriber,
                    IJSONResourceAPI,
                    IJSONResource
                )

            elif valid_dispatch.message_type == 'XML':

                return self.__api_processor(
                    valid_dispatch,
                    valid_response,
                    IXMLResourceSubscriber,
                    IXMLResourceAPI,
                    IXMLResource
                )


@implementer(IDispathcherResultHelper)
class DispathcherResultHelper(object):

    def __init__(self, factory):
        self.__logger = Logger()
        self.factory = factory

    def result_validation(self, sender=None, drop=None, section='TCP'):

        if IValidator.providedBy(self.factory):

            self.__logger.warning('{} Message is invalid: {}'.format(section, self.factory.message))

            if drop is not None:
                drop()

            else:
                return 'message is invalid'

        else:

            if self.factory:

                self.__logger.info('{} Response: {}'.format(section, self.factory))

                if IJSONResource.providedBy(self.factory):

                    if sender is not None:
                        sender(self.factory.to_json())

                    else:
                        return self.factory.to_json()

                elif IXMLResource.providedBy(self.factory):

                    if sender is not None:
                        sender(str(self.factory.to_xml()))

                    else:
                        return str(self.factory.to_xml())

                elif isinstance(self.factory, Deferred):

                    def deferred_response(response):

                        if sender is not None:
                            sender(response.to_json())

                    def deferred_response_error(err):

                        self.__logger.error('Cannot send message to user: {}'.format(
                            err
                        ))

                        return False

                    self.factory.addCallback(deferred_response)
                    self.factory.addErrback(deferred_response_error)

            else:

                self.__logger.warning('{}: This message was not be dispatched'.format(section))
                drop()

gsm = getGlobalSiteManager()
gsm.registerAdapter(Dispatcher)