from twisted.application import service

from NetCatKS.Components import ComponentsRegistration
from NetCatKS.NetCAT import DefaultFactory, IDefaultService, DefaultLineReceiver
from NetCatKS.NetCAT import IDefaultAutobahnService, AutobahnDefaultFactory

components = ComponentsRegistration().init()

mservice = service.MultiService()

apps = [
    IDefaultAutobahnService(AutobahnDefaultFactory(
        protocol='ws',
        name='TEST WAMP',
        port=8080,
        belong_to=mservice
    )),

    IDefaultService(DefaultFactory(
        protocol=DefaultLineReceiver,
        name='Test Server',
        port=11222,
        belong_to=mservice
    ))

]

for app in apps:
    app.start()

application = service.Application("NETCAT DEMO")

# Connect our MultiService to the application, just like a normal service.
mservice.setServiceParent(application)

# application = IDefaultAutobahnService(AutobahnDefaultFactory(
#     protocol='ws',
#     name='TEST WAMP',
#     port=8080,
#     parent=mservice
# )).start()
#
# application = IDefaultService(DefaultFactory(
#     protocol=DefaultLineReceiver,
#     name='Test Server',
#     port=11222,
#     parenti=mservice
# )).start()
#
