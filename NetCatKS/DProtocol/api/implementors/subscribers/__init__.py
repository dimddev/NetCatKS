"""
Base subscribers for a Dynamic Protocols implementations
"""

from zope.component import adapts
from zope.interface import implementer, classImplementsOnly

from NetCatKS.DProtocol.api.interfaces.subscribers import IBaseResourceSubscriber, IJSONResourceSubscriber
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
    def _get_all_keys_helper(req, temp, key, counter):

        if not req:
            temp.append('-{}'.format(key))

        else:
            temp.append('{}{}'.format(counter * '-', key))

        return temp

    def _get_all_keys(self, data=None, **kwargs):

        """
        This function gets all keys from dict recursively
        :param data:
        :type data: dict

        :return: list of keys
        """

        counter = kwargs.get('counter', False)

        # if data is set means recursion or external dict
        if data and isinstance(data, dict):

            _req = True
            in_data = data

        else:

            _req = False

            validate = kwargs.get('validate', True)
            in_data = self.to_dict(validate=validate)

        temp = []

        if in_data:

            for key in in_data.keys():

                j = counter or 1

                if isinstance(in_data[key], dict):

                    temp = BaseProtocolSubscriber._get_all_keys_helper(_req, temp, key, j)
                    j += 1

                    # recursion
                    temp += self._get_all_keys(in_data[key], counter=j)

                else:
                    temp = BaseProtocolSubscriber._get_all_keys_helper(_req, temp, key, j)

        return temp

    def compare(self):

        if isinstance(self.adapter.response, dict):

            _self = self._get_all_keys(self.protocol.to_dict(), validate=False)
            _self.sort()

            other = self._get_all_keys(self.adapter.response, validate=False)
            other.sort()

            if _self == other:
                return self.protocol.to_object(self.adapter.response)

        else:

            return False


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
