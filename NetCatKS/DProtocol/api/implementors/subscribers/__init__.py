"""
Base subscribers for a Dynamic Protocols implementations
"""

import traceback
import json
import xmltodict

from zope.component import adapts
from zope.interface import implementer, classImplementsOnly

from NetCatKS.DProtocol.api.interfaces.subscribers import IBaseResourceSubscriber, IJSONResourceSubscriber
from NetCatKS.DProtocol.api.interfaces.subscribers import IXMLResourceSubscriber
from NetCatKS.Validators import IValidatorResponse
from NetCatKS.Logger import Logger

__author__ = 'dimd'


@implementer(IBaseResourceSubscriber)
class BaseProtocolSubscriber(object):

    """
    This class providing a functionality that will compare the candidate request against
    the selected candidate protocol
    """

    def __init__(self, adapter):
        """

        :param adapter IJSONResource
        """

        try:

            getattr(self, 'protocol')

        except AttributeError:
            raise AttributeError('Wrong implementation, you must subclass the protocol attribute')

        else:

            self.protocol = getattr(self, 'protocol')
            self.adapter = adapter

        super(BaseProtocolSubscriber, self).__init__()

    @staticmethod
    def compare_debug(level, in_dict, host_proto):

        """
        For debug usage only

        :param level:
        :param in_dict:
        :param host_proto:

        :return: void

        """

        logger = Logger()
        logger.debug('COMPARE LEVEL {}'.format(level))
        logger.debug('IN_DICT: {}'.format(in_dict))
        logger.debug('HOST_PROTO: {}'.format(host_proto))
        logger.debug('END COMPARE LEVEL {}'.format(level))

    def compare(self):

        """
        Will compare the protocol against adapter

        :return: dynamic created protocol from the request or False

        """

        # NETODO - to be refactored as two methods

        # xml

        if isinstance(self.adapter, tuple):

            try:

                self.adapter = self.adapter[0]

            except IndexError as i_error:

                print i_error.message
                print traceback.format_exc()
                return False

        if isinstance(self.adapter.response, str):

            try:

                self.adapter.response = xmltodict.parse(self.adapter.response)

                # this dirty trick will make convert OrderedDict to normal
                # because our DProtocol API currently does not support OrderDict
                # when we starting to support XML with name spaces have to be extended

                self.adapter.response = json.dumps(self.adapter.response)
                self.adapter.response = json.loads(self.adapter.response)

            except Exception as c_error:

                print c_error.message
                print traceback.format_exc()

                return False

        # normal case

        self.protocol.__init__()

        in_dict = self.protocol.get_all_keys(self.adapter.response)
        host_proto = self.protocol.get_all_keys(self.protocol.to_dict())

        in_dict.sort()
        host_proto.sort()

        # self.compare_debug(1, in_dict, host_proto)

        if ''.join(in_dict) == ''.join(host_proto):
            return self.protocol.to_object(self.adapter.response)

        # else:
        #
        #     in_dict = self.adapter.response.keys()
        #     host_proto = self.protocol.to_dict().keys()
        #
        #     in_dict.sort()
        #     host_proto.sort()
        #
        #     # self.compare_debug(2, in_dict, host_proto)
        #
        #     if ''.join(in_dict) == ''.join(host_proto):
        #         return self.protocol.to_object(self.adapter.response)
        #
        #     return False


class DProtocolSubscriber(BaseProtocolSubscriber):

    """
    This class is designed to be sub classed not for directly usage
    """

    adapts(IValidatorResponse)

    def __init__(self, adapter):

        """
        :param adapter IJSONResource
        """

        super(DProtocolSubscriber, self).__init__(adapter)


classImplementsOnly(DProtocolSubscriber, IJSONResourceSubscriber)


class DProtocolXMLSubscriber(BaseProtocolSubscriber):

    """
    This class is designed to be sub classed not for directly usage
    """

    adapts(IValidatorResponse)

    def __init__(self, adapter):

        """
        :param adapter IJSONResource
        """

        super(DProtocolXMLSubscriber, self).__init__(adapter)

classImplementsOnly(DProtocolXMLSubscriber, IXMLResourceSubscriber)
