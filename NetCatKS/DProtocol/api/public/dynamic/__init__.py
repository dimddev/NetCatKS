__author__ = 'dimd'

from ...interfaces.dymanic import IDynamicProtocolInterface
from ...implementors.dynamic import DynamicProtocolImplementor

from zope.interface.verify import verifyObject
from zope.interface.exceptions import BrokenImplementation


class DynamicProtocol(DynamicProtocolImplementor):

    def __init__(self, **kwargs):

        super(DynamicProtocol, self).__init__(**kwargs)

        try:

            verifyObject(IDynamicProtocolInterface, self)

        except BrokenImplementation as e:
            print e.message
