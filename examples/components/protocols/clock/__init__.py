
from __future__ import absolute_import

__author__ = 'NetCatKS auto generator at 2015-10-02 16:03:11.224681'

from zope.interface import Interface, Attribute, implementer
from zope.component import getGlobalSiteManager

from NetCatKS.DProtocol import BaseProtocolActions, DProtocolSubscriber
from NetCatKS.Dispatcher import IJSONResource
    

class ITimeInterface(Interface):
        
    clock = Attribute("Comments going here")
        

@implementer(ITimeInterface)
class TimeImplementer(BaseProtocolActions):

    def __init__(self, **kwargs):
        
        self.__clock = None
        
    @property
    def clock(self):
        return self.__clock

    @clock.setter
    def clock(self, clock):
        self.__clock = clock
            

@implementer(IJSONResource)
class TimeProtocol(TimeImplementer):

    def __init__(self, **kwargs):

        super(TimeProtocol, self).__init__(**kwargs)
            

class TimeProtocolSubscriber(DProtocolSubscriber):

    def __init__(self, adapter):

        self.adapter = adapter
        self.protocol = TimeProtocol()


gsm = getGlobalSiteManager()
gsm.registerSubscriptionAdapter(TimeProtocolSubscriber)
