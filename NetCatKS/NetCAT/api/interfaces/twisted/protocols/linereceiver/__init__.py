"""
A module interface for a Twisted LineReceiver default implementation
"""

from zope.interface import Interface

__author__ = 'dimd'


class IDefaultLineReceiver(Interface):
    """
    The implementer has to provide functionality related for twisted LineReceiver
    """
