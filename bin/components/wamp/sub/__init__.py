

from NetCatKS.Components.api import IUserGlobalSubscriber
from NetCatKS.Dispatcher import IJSONResource

from zope.interface import implementer
from zope.component import adapts


@implementer(IUserGlobalSubscriber)
class GlobalSubscriberCallBack(object):

    adapts(IJSONResource)

    def __init__(self, adapt=None):
        self.adapt = adapt

    def subscribe(self):
        print 'MESSAGE FROM GLOBAL SUB CALLBACK: {}'.format(self.adapt)
    