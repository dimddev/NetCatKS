
from twisted.application import service

from NetCatKS.NetCAT import IDefaultWebService, DefaultWebFactory
from NetCatKS.Components import ComponentsRegistration
from NetCatKS.NetCAT import DefaultFactory, IDefaultService
from NetCatKS.NetCAT import IDefaultAutobahnService, AutobahnDefaultFactory
from NetCatKS.NetCAT import IDefaultWSService, DefaultWSFactory

components = ComponentsRegistration().init()


multi_service = service.MultiService()

apps = [

    IDefaultService(DefaultFactory(
        config=components.config.get_tcp(),
        belong_to=multi_service
    )),

    IDefaultAutobahnService(AutobahnDefaultFactory(
        config=components.config.get_wamp(),
        belong_to=multi_service
    )),

    IDefaultWebService(DefaultWebFactory(
        config=components.config.get_web(),
        belong_to=multi_service
    )),

    IDefaultWSService(DefaultWSFactory(
        config=components.config.get_ws(),
        belong_to=multi_service
    ))
]

for app in apps:
    app.start()

application = service.Application("NetCatKS DEMO")
multi_service.setServiceParent(application)
