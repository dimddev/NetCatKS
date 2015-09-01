__author__ = 'dimd'

from zope.interface import implementer
from zope.component import adapts
from ....public import IDispatcher, IJSONResource


@implementer(IDispatcher)
class JSONDispatcher(object):
    """
    Will dispatch every json
    """
    adapts(IJSONResource)

    def __init__(self, json):
        pass

    def dispatch(self):
        pass
