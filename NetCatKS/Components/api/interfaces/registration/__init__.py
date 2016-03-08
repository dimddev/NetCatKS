"""
A module related for a component registration
"""

from zope.interface import Interface
__author__ = 'dimd'


class IComponentRegistrator(Interface):

    """
    A base interface for our ComponentRegistrator API
    """

    def make(**kwargs):
        """
        combined register component, factories and adapters
        :param kwargs:
        :return:
        """
