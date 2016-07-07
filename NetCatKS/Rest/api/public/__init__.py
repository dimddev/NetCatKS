from NetCatKS.Rest.api.implementers import RestResource


class Rest(RestResource):

    """
    This class is our entry point for accessing REST API's, it provide simple and easy way
    to access REST resources in async way
    """

    def __init__(self, **kwargs):

        super(Rest, self).__init__(**kwargs)
        self.uri = kwargs.get('uri', '/')

    def post(self, **kwargs):

        """
        this method provide POST request.

        :param kwargs:
            dict with two required keys: *uri* - the rest resources uri address
            and - *data* - which is data to be posted

        :return: rest defered object
        """

        return self.set_uri(kwargs.get('uri', self.uri)).rest_post(data=kwargs['data'])

    def get(self, **kwargs):

        """
        this method provide GET request.

        :param kwargs:
            dict with one required keys: *uri* - the rest resources uri address

        :return: rest defered object
        """

        return self.set_uri(kwargs.get('uri', self.uri)).rest_get()

    def put(self, **kwargs):
        """
        this method provide PUT request.

        :param kwargs:
            dict with two required keys: *uri* - the rest resources uri address
            and - *data* - which is data to be posted

        :return: rest defered object
        """

        return self.set_uri(kwargs.get('uri', self.uri)).rest_put(data=kwargs['data'])
