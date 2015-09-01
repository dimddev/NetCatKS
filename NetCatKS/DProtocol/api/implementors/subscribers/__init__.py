__author__ = 'dimd'

from zope.component import adapts
from zope.interface import implementer


from .....Validators import IValidatorResponse
from .....Dispatcher import IJSONResource


@implementer(IJSONResource)
class DProtocolSubscriber(object):

    """
    This class is designed to be subclassed not for directly usage
    """
    adapts(IValidatorResponse)

    def __init__(self, adapter):
        """

        :param adapter IValidatorResponse
        """
        self.adapter = adapter

    def compare(self):

        self.adapter.response.keys().sort()

        # the protocol comes from our subclass
        self.protocol.to_dict().keys().sort()

        if ''.join(self.adapter.response.keys()) == ''.join(self.protocol.to_dict().keys()):
            return self.protocol.to_object(self.adapter.response)

        else:

            return False