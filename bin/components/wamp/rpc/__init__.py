from NetCatKS.Components import BaseWampComponent
from autobahn import wamp
from datetime import datetime


from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.component import getGlobalSiteManager


class TestComponentWamp(BaseWampComponent):

    def __init__(self):
        super(TestComponentWamp, self).__init__()

    @wamp.register(u'get_time')
    def pub_news(self):
        t = datetime.now()
        print t
        return str(t)


gsm = getGlobalSiteManager()

factory = Factory(TestComponentWamp, TestComponentWamp.__name__)
gsm.registerUtility(factory, IFactory, TestComponentWamp.__name__.lower())
