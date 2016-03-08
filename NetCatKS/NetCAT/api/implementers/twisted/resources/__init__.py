"""
A module that represent our web resources
"""

from twisted.web.resource import Resource

from NetCatKS.NetCAT.api.interfaces.twisted.recources import IDefaultWebResource
from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultWebFactory
from NetCatKS.Logger import Logger

from zope.interface import classImplementsOnly
from zope.component import adapts, getGlobalSiteManager

from NetCatKS.Dispatcher import IDispatcher, DispathcherResultHelper
from NetCatKS.Validators import Validator

__author__ = 'dimd'


class BaseWebMethods(object):

    """
    A Base class for our web methods, currently we having PUT, GET and POST
    """

    def __init__(self):
        """
        The constructor will init our logger
        :return: void
        """
        self.__logger = Logger()

    def render_PUT(self, request):
        """
        The put method is still not implemented
        :param request:
        :return:
        """
        return 'ok'

    def render_GET(self, request):
        """

        :param request:
        :return:
        """

        print request
        return """
<!DOCTYPE html>
<head>
    <title>IplayNinja</title>
    <link rel="stylesheet" type="text/css" href="ninja.css">
</head>
<body>
    <h1>Hello from NetCatKS Web</h1>
</body>
</html>
"""

    def render_POST(self, request):

        """

        :param request:
        :return:
        """

        result = IDispatcher(Validator(request.content.read())).dispatch()
        result_response = DispathcherResultHelper(result)
        return result_response.result_validation(None, None, 'WEB')


class DefaultWebResource(Resource):
    """
    Our default web resource will be extended runtime based on the configuration, that meaning
    all methods as PUT, GET, POST will be attached to this cass from our BaseWebMethods
    Our default resource it self is registered as subscriber and adapts IDefaultWebFactory
    """
    adapts(IDefaultWebFactory)

    isLeaf = True

    def __init__(self, factory):
        """

        :param factory:
        :return: void
        """

        base = BaseWebMethods()
        self.__logger = Logger()

        for meth in factory.config.http_methods:

            try:

                name = 'render_{}'.format(meth)
                web_resource = getattr(base, name)

            except AttributeError as e:

                allow_methods = [
                    render.replace('render_', '') for render in base.__class__.__dict__ if render.startswith('render')
                ]

                print('[ !!!!! Warning: ] Ivalid web methods was provided, available are: {}, error: {}'.format(
                    ', '.join(allow_methods), e
                ))

            else:
                setattr(DefaultWebResource, name, web_resource)

        Resource.__init__(self)


classImplementsOnly(DefaultWebResource, IDefaultWebResource)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultWebResource)
