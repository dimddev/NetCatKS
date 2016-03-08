"""
Interface that represent our storage
"""

from zope.interface import Interface, Attribute

__author__ = 'dimd'


class IProtocolStogareInterface(Interface):

    """
    This interface define our session storage
    Every custom storage have to implement this Interface
    """

    session = Attribute(""" Container for our session """)
