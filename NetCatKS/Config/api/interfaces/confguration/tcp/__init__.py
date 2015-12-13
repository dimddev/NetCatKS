"""
A module contains an interface which represent our TCP part of config
"""

from zope.interface import Interface, Attribute

__author__ = 'dimd'


class ITcp(Interface):

    """
    Interface for a TCP configuration
    """

    port = Attribute('A TCP port')
    service_name = Attribute('A TCP Service Name')
    tcp_back_log = Attribute('A TCP Back log')
