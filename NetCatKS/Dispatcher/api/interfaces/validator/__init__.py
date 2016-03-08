"""
A module for a dispatch validation interface
"""
from zope.interface import Interface
__author__ = 'dimd'


class IDispatchAPIValidator(Interface):

    """
    A Base interface for validation
    """
    def validate(check_one, check_two):

        """
        validate whether in_dict.keys.sort() is equal to self.to_dict().keys().sort()
        :param in_dict: dict
        :return: bool
        """
