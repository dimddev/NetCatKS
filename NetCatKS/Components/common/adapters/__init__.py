"""
A module that contains a helper and base class for some dynamic and shared adapters
"""
from zope.interface import alsoProvides
from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter
__author__ = 'dimd'


class AdapterProxyGetter(object):
    """
    This class overwrites __getattr__ magic method and provides a easy way to deal
    with multiadapters ( combine many object into one) we will walking through all adaptee
    object and will trying to find to where belong, the will be returned so we play here with
    ProxyGetter
    """
    __debug = False

    def __init__(self, *args):

        """
        Set init arguments and call a super
        :param args:

        :return: void
        """
        self._adapters = args

        super(AdapterProxyGetter, self).__init__()

    def __getattr__(self, name):

        """
        returning matched attribute or method otherwise raise AttributeError

        :param name: list of adaptee objects

        :return: matched attribute or method or raise AttributeError
        """

        checker = []
        obj = None

        for obj in self._adapters:

            # for normal attributes
            if obj.__dict__.get(name, None) is not None:

                return obj.__dict__.get(name)

            # for properties
            elif getattr(obj, name) and not callable(getattr(obj, name)):
                return getattr(obj, name)

            # for methods
            elif callable(getattr(obj, name)):

                def proxy(*args, **kwargs):

                    """
                    Will make a fake method
                    :param args:
                    :param kwargs:

                    :return: method result
                    """
                    setattr(self, obj.__class__.__name__.lower(), obj)
                    return getattr(obj, name)(*args, **kwargs)

                return proxy

        if len(checker) == len(self._adapters):

            error = type(
                'InvalidAttribute',
                (object,),
                {
                    'message': 'attribute {} does not exist'.format(name),
                    'error': True,
                    name: False
                }
            )

            alsoProvides(error, IVirtualAdapter)
            return error()

__all__ = [
    'AdapterProxyGetter'
]
