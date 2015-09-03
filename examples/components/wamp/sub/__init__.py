from NetCatKS.NetCAT.api.interfaces import IUserGlobalSubscriber, IGlobalSubscribeMessage

from zope.interface import implementer
from zope.component import adapts


@implementer(IUserGlobalSubscriber)
class GlobalSubscriberCallBackWamp(object):

    adapts(IGlobalSubscribeMessage)

    def __init__(self, adapt=None):
        self.adapt = adapt

    def subscribe(self):
        print self.adapt.message

