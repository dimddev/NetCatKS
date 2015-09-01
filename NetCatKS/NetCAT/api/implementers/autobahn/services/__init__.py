__author__ = 'dimd'

from ...twisted.services import DefaultService


class DefaultAutobahnService(DefaultService):

    def __init__(self, factory):

        super(DefaultAutobahnService, self).__init__(factory)

    def start():
        pass
