__author__ = 'dimd'


from ....interfaces.message import IMessage
from ..default import BaseValidator

from zope.component import adapts
from zope.component import getGlobalSiteManager

from lxml.html import document_fromstring


class HTMLValidator(BaseValidator):

    adapts(IMessage)

    def __init__(self, validate_msg):
        super(HTMLValidator, self).__init__(validate_msg)

    def validate(self):

        try:
            __html = document_fromstring(self.validate_msg.message)

        except Exception as e:

            return self

        else:

            try:

                head = __html.head
                body = __html.body

            except IndexError:
                return self

            else:

                self.is_valid = True
                self.message_type = 'HTML'
                self.message = self.validate_msg.message

                return self

gsm = getGlobalSiteManager()
gsm.registerSubscriptionAdapter(HTMLValidator)