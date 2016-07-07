import urllib
from twisted.web import client
from NetCatKS.Logger import Logger

__author__ = 'dimd'


class RestResource(object):

    """
    RestResource provides functionality defined in IRestResource and its own
    methods which are common for our operations
    """

    __debug = True

    __result = None

    __logger = None

    def __new__(cls, **kwargs):

        """
        __new__ is called before __init__ so there we place our logic that prevent
        direct access of this Resource, that means you have to subclass it

        :param cls:
        :param args: list of args
        :param kwargs: dict
        :return: subclass object
        """
        if cls is RestResource:
            raise TypeError("<RestResource> must be subclassed")
        return object.__new__(cls)

    def __init__(self, **kwargs):

        """
        constructor can set our uri

        :param uri: http uri
        :return: void
        """
        RestResource.__logger = Logger()

        self.uri = kwargs.get('uri', '/')
        self.mime_type = kwargs.get('mime_type', 'application/x-www-form-urlencoded')

        self.rest_db = kwargs.get('rest_db', None)
        self.rest_token = kwargs.get('rest_token', None)

        assert self.rest_db is not None
        assert self.rest_token is not None

    def request_success(self, result):

        """
        Callback fired when we have returned success with our request
        a good place to make some custom logic

        :param result: clear data from defer
        :return: modified or not result
        """
        if RestResource.__debug is True:
            RestResource.__logger.info('REST REQUEST SUCCESSFUL')

        return result

    def request_error(self, result, uri):
        """
        Callback fired when we have some returned error from our request

        :param result: clear data from defer
        :return: result
        """
        if RestResource.__debug is True:
            RestResource.__logger.error('REST RESULT ERROR: {} URI: {}'.format(
                result.getErrorMessage(), self.rest_db + uri)
            )

        return False

    def set_uri(self, uri):
        """
        Set the request URI

        :param uri: http uri
        :return: self
        """
        self.uri = uri
        return self

    def rest_get(self):
        """
        This method works as proxy and point to actual functionality
        int self_send_request

        :return: self._send_request
        """
        return self._send_request('GET')

    def rest_post(self, **kwargs):

        """
        This method works as proxy and point to actual functionality
        int self_send_request

        :param kwargs: dict of args
        :return: self._send_request
        """

        try:

            post_data = urllib.urlencode(kwargs.get('data'))
            return self._send_request('POST', post_data, self.mime_type)

        except Exception as e:
            RestResource.__logger.error('REST POST ERROR: {}'.format(e.message))

    def rest_put(self, **kwargs):

        """

        This method works as proxy and point to actual functionality
        int self_send_request

        TODO: this method is not tested

        :param kwargs: dict
        :param mime_type: RFC mime_type
        :return: self._send_request
        """
        put_data = urllib.urlencode(kwargs.get('data'))
        return self._send_request('PUT', put_data, self.mime_type)

    def rest_delete(self, **kwargs):
        """
        implement IRestResource.put

        This method works as proxy and point to actual functionality
        int self_send_request

        TODO: NOT IMPLEMENTED YET

        :param kwargs: dict of args
        :return: self._send_request
        """
        pass

    def _send_request(self, method, data='', mime_type=None):
        """
        This methods take care about all actions

        :param method: GET, POST, PUT, DELETE
        :param data: dict of args
        :param mime_type: RFC mime type
        :return: rest defer
        """

        headers = dict()

        headers['Authorization'] = 'Token {}'.format(self.rest_token)

        if mime_type:
            headers['Content-Type'] = mime_type

        # POST + PUT
        if data and method == 'POST' or method == 'PUT':

            headers['Content-Length'] = str(len(data))

            req = client.getPage(self.rest_db + self.uri, method=method, postdata=data, headers=headers)

        # ONLY GET - no data
        elif method == 'GET':
            req = client.getPage(self.rest_db + self.uri, method=method, headers=headers)

        # DIMDTODO PLACE FOR FUTURE DELETE METHOD BUT MAY BE NOT : )
        else:
            pass

        req.addCallback(self.request_success)
        req.addErrback(self.request_error, self.uri)
        return req
