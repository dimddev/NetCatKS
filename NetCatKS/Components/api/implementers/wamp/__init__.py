"""
A helper class that provides a base wamp component functionality
"""
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPComponent, IWAMPResource
from zope.interface import implementer
from zope.component import adapts

__author__ = 'dimd'


@implementer(IWAMPComponent)
class BaseWampComponent(object):
    """
    We will adapt only a API from a IWAMPResource type
    """
    adapts(IWAMPResource)

    def __init__(self):
        """
        Class calling a super and set a session to None
        :return:
        """
        super(BaseWampComponent, self).__init__()
        self.session = None

    def set_session(self, sesison):

        """
        Wamp session setter - providing an attribute that
        representing an active wamp session
        :param sesison:

        :return: void
        """
        self.session = sesison
