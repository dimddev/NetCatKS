"""
A module that providing a validation of a XML Format
"""
from lxml import etree

from zope.component import adapts
from zope.component import getGlobalSiteManager

from NetCatKS.Validators.api.interfaces.message import IMessage
from NetCatKS.Validators.api.implementers.validators.default import BaseValidator


__author__ = 'dimd'


class XMLValidator(BaseValidator):

    """
    A class that providing a XML validation
    """
    adapts(IMessage)

    def __init__(self, validate_msg):

        """
        A constructor just calling a super

        :param validate_msg:
        :return: void
        """
        super(XMLValidator, self).__init__(validate_msg)

    def validate(self):

        """
        A default validate method

        :return: self
        """

        try:

            _ = etree.fromstring(self.validate_msg.message)

        except Exception as e:
            return self

        else:

            self.is_valid = True
            self.message_type = 'XML'
            self.message = self.validate_msg.message

            return self

gsm = getGlobalSiteManager()
gsm.registerSubscriptionAdapter(XMLValidator)
