"""
A container for our common and helper classes
"""
from zope.component import createObject
from NetCatKS.Components.common.loaders import BaseLoader

__author__ = 'dimd'


def get_factory(name):
    return createObject(name)

__all__ = [
    'BaseLoader',
    'get_factory'
]
