__author__ = 'dimd'

from ..interfaces import IJSONResource, IXMLResource, IHTMLResource
from ..interfaces.dispatcher import IDispatcher

from ..implementers.dispatcher import Dispatcher

__all__ = [
    'IJSONResource',
    'IXMLResource',
    'IHTMLResource',
    'IDispatcher',
    'Dispatcher'
]

