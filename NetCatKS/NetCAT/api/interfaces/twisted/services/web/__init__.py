"""
A module interface for a Twisted default WEB Services
"""
from zope.interface import Interface, Attribute

__author__ = 'dimd'


class IDefaultWebService(Interface):
    """
    A class for a Twisted default WEB Services
    """
    factory = Attribute('attribute that will adapt IDefaultWebFactory')

    def get_service():
        """
        return web root
        :return:
        """

    def start():
        """
        start default web service
        :return:
        """
