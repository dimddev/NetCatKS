__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IDefaultAutobahnFactory(Interface):

    protocol = Attribute('WAMP protocol can be ws or wss')
    name = Attribute('Service name')
    port = Attribute('WS port usually crossbar WS')
    host = Attribute('WS host')
    path = Attribute('WS path for example: ws://localhost/path')
    realm = Attribute('WS Realm')
