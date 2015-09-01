__author__ = 'dimd'

from ...interfaces.filters import IProtocolFiltersInterface
from zope.interface import implementer


@implementer(IProtocolFiltersInterface)
class ProtocolFiltersImplementor(object):

    @staticmethod
    def check_for_float_and_int(check):

        """
        Implements `session.interface.filters.ISessionFiltersInterface.check_for_float_and_int
        :param check:
        :return:
        """

        if type(check) is not float and type(check) is not int:

            raise Exception('API Error: incorrect configure, input must be float or int')

        else:
            return True

    @staticmethod
    def check_for_float(check):

        """

        :param check:
        :return:
        """

        if type(check) is not float:

            raise Exception('API Error: incorrect configure, input must be float')

        else:
            return True

    @staticmethod
    def check_for_int(check):

        """

        :param check:
        :return:
        """
        if type(check) is not int:
            raise Exception('API Error: incorrect configure, input must be int')

        else:
            return True

    @staticmethod
    def check_for_list(check):

        """

        :param check:
        :return:
        """
        if type(check) is not list:
            raise Exception('API Error: incorrect configure, input must be list')

        else:
            return True


    @staticmethod
    def check_for_bool(check):

        """

        :param check:
        :return:
        """
        if type(check) is not bool:
            raise Exception('API Error: incorrect configure, input must be bool')

        else:
            return True

    @staticmethod
    def check_for_dict(indict):

        """

        :param indict:
        :return:
        """

        if type(indict) is not dict:
            raise Exception('API Error: incorrect congure, input must be dict')

        else:
            return True
