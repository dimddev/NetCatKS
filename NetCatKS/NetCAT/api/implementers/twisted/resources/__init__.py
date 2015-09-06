__author__ = 'dimd'

from twisted.web.resource import Resource

from NetCatKS.NetCAT.api.interfaces.twisted.recources import IDefaultWebResource
from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultWebFactory
from NetCatKS.Logger import Logger

from zope.interface import classImplementsOnly
from zope.component import adapts, getGlobalSiteManager

from NetCatKS.Dispatcher import IDispatcher, IJSONResource, IXMLResource
from NetCatKS.Validators import Validator, IValidator


class BaseWebMethods(object):

    def __init__(self):

        self.__logger = Logger()

    def render_PUT(self, request):

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

        if IValidator.providedBy(result):
            self.__logger.warning('WEB Message is invalid: {}'.format(result.message))
            return 'message is invalid'

        else:

            if result:

                if IJSONResource.providedBy(result):

                    return result.to_json()

                elif IXMLResource.providedBy(result):

                    return str(result.to_xml())

            else:

                self.__logger.warning('WEB: This message was not be dispatched')
                return ''


class DefaultWebResource(Resource):

    adapts(IDefaultWebFactory)

    isLeaf = True

    def __init__(self, factory, **kwargs):
        """

        :param factory:
        :param kwargs:
        :return:
        """

        base = BaseWebMethods()
        self.__logger = Logger()

        for meth in factory.config.get('WEB_METHODS'):

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
