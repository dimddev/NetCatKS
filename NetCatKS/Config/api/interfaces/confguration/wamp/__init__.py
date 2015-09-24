__author__ = 'dimd'

from zope.interface import Interface, Attribute

# "WAMP": {
#     "WS_USER": "wamp_ws_user",
#     "WS_NAME": "Default WAMP Component",
#     "WS_URL": "wss://localhost:8080/ws",
#     "WS_REALM": "realm1",
#     "WS_PORT": 8080,
#     "WS_PROTO": "wss",
#     "WS_RETRY_INTERVAL": 2,
#     "WS_PATH": "ws",
#     "WS_PASS": "wamp_ws_password",
#     "WS_IP": "localhost"
# }


class IWamp(Interface):

    user = Attribute('WAMP CRA User')
    password = Attribute('WAMP CRA password')
    service_name = Attribute('WAMP Service name')
    url = Attribute('WAMP url, can be secure or unsecure (wss or ws) wss://localhost:8080/ws')
    realm = Attribute('WAMP Realm')
    port = Attribute('Crossbar port')
    protocol = Attribute('WAMP protocol ws or wss')
    retry_interval = Attribute('If connection is lost, we will trying to reconnect via this interrval')
    path = Attribute('Pato from wamp url')
    hostname = Attribute('crossbar hostname')