__author__ = 'dimd'

from NetCatKS.Dispatcher.api.interfaces import IJSONResource
from NetCatKS.DProtocol.api.interfaces.actions import IBaseProtocolActionsInterface
from NetCatKS.DProtocol.api.interfaces.tdo import IDynamicTDO

from zope.component import adapts, getGlobalSiteManager
from zope.interface import implementer


@implementer(IDynamicTDO)
class DynamicTDO(object):

    adapts(IJSONResource)

    def __init__(self, factory):
        self.factory = factory

    def create_tdo(self, in_data):
        pass

    def to_tdo(self, in_data):

        deep = 0

        def inner(apidata, indata, deep):
            """

            :param apidata:
            :type apidata: dprotocol instance
            :param indata:
            :type indata: iterable
            :param deep: how deep I'm

            :return: dict
            """
            deep += 1

            # apidata is a dprotocol instance, predefined inside our backend as
            # DProtocol implementation in both way it inherit from BaseProtocolActions which provides
            # IBaseProtocolActionsInterface

            for k, v in apidata.to_dict().iteritems():

                # so if we meet attribute from IBaseProtocolActionsInterface type means it's a sub protocol
                # and we have to call inner
                if IBaseProtocolActionsInterface.providedBy(getattr(apidata, k)):
                    inner(getattr(apidata, k), indata, deep)

                else:

                    # otherwise we will looping over all items in indata
                    for ik, iv in indata.iteritems():

                        # 1. we checking whether the ik exist directly in our root dict of apidata
                        if ik in apidata.to_dict():

                            # if exist we get the value from apidata.to_dict().get(ik) with ik as key
                            indata[ik] = apidata.to_dict().get(ik)

                        elif type(iv) is dict:

                            # 2.if iv is a dict first we will trying to get the k apidata key
                            # from this dict

                            if k in iv:

                                # if exist will update the indata for this key
                                indata[ik].update({k: apidata.to_dict().get(k)})

                            else:

                                # else we pass the iv to our inner again for more
                                # nested structures
                                inner(apidata, iv, deep)
            return indata, deep

        result, deep = inner(self.factory, in_data, deep)

        return result


gsm = getGlobalSiteManager()
gsm.registerAdapter(DynamicTDO)
