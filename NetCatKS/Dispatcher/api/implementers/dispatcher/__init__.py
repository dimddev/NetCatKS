"""
A module that contain a main functionality for a NetCatKS
"""
from twisted.internet.defer import Deferred

from zope.interface import implementer
from zope.component import adapts, subscribers
from zope.component import getGlobalSiteManager
from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement

from NetCatKS.Dispatcher.api.interfaces.dispatcher import IDispatcher
from NetCatKS.Dispatcher.api.interfaces.dispatcher import IDispathcherResultHelper

from NetCatKS.Components import IJSONResource, IJSONResourceAPI, IJSONResourceRootAPI

from NetCatKS.DProtocol.api.interfaces.subscribers import IJSONResourceSubscriber

from NetCatKS.Validators.api.public import IValidator, ValidatorResponse

from NetCatKS.Logger import Logger

__author__ = 'dimd'


class NonRootAPI(object):

    """
    An API that will check for a Non Root API's
    """

    def __init__(self, comp):

        """
        A NonRootAPi constructor will init a logger and a comp property for an object
        that have to be compare with the existing registered protocols

        :param comp:
        :type comp: an input object as DynamicProtocol

        :return: void
        """

        self.comp = comp
        self.__logger = Logger()

    def check(self):

        """
        Will trying to match the candidate Non Root API
        check IJSONResourceAPI for more info

        :return: False if not success otherwise the response from matched API.method()
        """

        for api in subscribers([self.comp], IJSONResourceAPI):

            if api.__class__.__name__.lower() in self.comp.to_dict().keys():

                self.__logger.debug('Candidate API {} for {}'.format(
                    api.__class__.__name__,
                    self.comp.__class__.__name__
                ))

                candidate_api_name = self.comp.to_dict().get(api.__class__.__name__.lower())

                try:
                    # execute the candidate API method
                    # and return the result
                    candidate_api_result = getattr(api, candidate_api_name)()

                except AttributeError as e:

                    msg = 'Candidate API {} for {} does not implement method {} error: {}'

                    self.__logger.warning(msg.format(
                        api.__class__.__name__,
                        self.comp.__class__.__name__,
                        candidate_api_name,
                        e.message
                    ))

                else:

                    self.__logger.info('Successful apply API {} for {}'.format(
                        api.__class__.__name__,
                        self.comp.__class__.__name__
                    ))

                    return candidate_api_result

        return False


class RootAPI(object):
    """
    An API that implements an IJSONResourceRootAPI
    """
    def __init__(self, comp):

        """
        A RootAPI constructor will init an logger and will initialize a public attribute
        - self.comp which representing an input object as DynamicProtocol

        :param comp:
        :type comp: DynamicProtocol

        :return: void
        """
        self.comp = comp
        self.__logger = Logger()

    def check(self):

        """
        Will trying to get a RootAPI and if match one will fired a process_factory
        of an implementation API

        :return: False if not success otherwise the response from process_factory
        """
        for api in subscribers([self.comp], IJSONResourceRootAPI):

            if api.__class__.__name__.lower() in self.comp.to_dict().keys():

                self.__logger.debug('Candidate API {} for {}'.format(
                    api.__class__.__name__,
                    self.comp.__class__.__name__
                ))

                self.__logger.info('Successful apply API {} for {}'.format(
                    api.__class__.__name__,
                    self.comp.__class__.__name__
                ))

                return api.process_factory()

        return False


@implementer(IDispatcher)
class Dispatcher(object):

    """
    Our Main dispatcher, Will trying to dispatch the request to API which provides functionality for it.
    The Dispatcher also adapts IValidator
    """

    adapts(IValidator)

    def __init__(self, validator):

        """
        The constructor will init a logger and will init a public attribute - self.validator
        that is a validated requests, here we have to determinate which protocol and API have
        to process this request

        :param validator:
        :type validator: IValidator

        :return: void
        """

        self.validator = validator
        self.__logger = Logger()

    def __api_processor(self, valid_dispatch, valid_response, isubscriber):

        """

        Will loop through a valid response objects and will compare it to a registered
        protocol subscribers

        :param valid_dispatch:
        :param valid_response:
        :param isubscriber:

        :return: The chosen API or False
        """
        for sub in subscribers([valid_response], isubscriber):

            self.__logger.debug('Matched request subscribers: {}'.format(sub.__class__.__name__))

            try:

                verifyObject(isubscriber, sub)

            except DoesNotImplement as e:

                self.__logger.warning('Incorrect implementation: {}'.format(e))

            else:

                comp = sub.compare()

                if comp is not False and IJSONResource.providedBy(comp):

                    self.__logger.debug('Signature compare to {}'.format(comp.__class__.__name__))

                    # trying to resolve API that will deal with these request

                    if len(comp.to_dict().keys()) > 1:
                        # process request without root element
                        return NonRootAPI(comp).check()

                    else:
                        # root element
                        return RootAPI(comp).check()

        # if there are no one subsciber from IJSONResource

        self.__logger.warning('The request {} from type {} was not recognized as a structure or an API'.format(
            valid_response.response,
            valid_dispatch.message_type
        ))

        return False

    def dispatch(self):

        """
        When request is happening first will be validated,
        if valid_dispatch is False means we do not support this data type. You have to write your custom
        validator(s) inside components/validators

        :return: The response or False
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
                    IJSONResourceSubscriber
                )


@implementer(IDispathcherResultHelper)
class DispathcherResultHelper(object):

    """
    A helper class that care about of the result and the response of the request
    """

    def __init__(self, factory):

        """
        Just settings
        :param factory:
        :return: void
        """

        self.__logger = Logger()
        self.factory = factory

    @staticmethod
    def deferred_response(response, sender):

        """
        Care about global defered response
        :param response: response from defer operation
        :param sender: TBA

        :return: void
        """
        if sender is not None:
            sender(response.to_json())

    def deferred_response_error(self, err):

        """
        fired if global defered response fail
        :param err:

        :return: False
        """
        self.__logger.error('Cannot send message to user: {}'.format(
            err
        ))

        return False

    def result_validation(self, sender=None, drop=None, section='TCP'):

        """
        A Result Helper more info TBA

        :param sender:
        :param drop:
        :param section:

        :return: mixin
        """

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

                elif isinstance(self.factory, Deferred):

                    self.factory.addCallback(self.deferred_response, sender)
                    self.factory.addErrback(self.deferred_response_error)

            else:

                self.__logger.warning('{}: This message was not be dispatched'.format(section))
                drop()

gsm = getGlobalSiteManager()
gsm.registerAdapter(Dispatcher)
