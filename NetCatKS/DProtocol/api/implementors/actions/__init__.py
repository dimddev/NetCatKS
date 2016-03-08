"""
The Base actions for a DProtocol API. All sub protocols and main protocols have to use
this as base class
"""

import json
import xmltodict

from zope.interface import implementer
from zope.interface.exceptions import DoesNotImplement


from NetCatKS.DProtocol.api.interfaces.actions import IBaseProtocolActionsInterface
from NetCatKS.DProtocol.api.interfaces.storage import IProtocolStogareInterface
from NetCatKS.DProtocol.api.public.storage import ProtocolStorage
from NetCatKS.DProtocol.api.implementors.filters import ProtocolFiltersImplementor


__author__ = 'dimd'


@implementer(IBaseProtocolActionsInterface)
class BaseProtocolActionsImplementor(ProtocolFiltersImplementor):

    """
    This class provides implementation of `session.interfaces.actions.IBaseSessionActionsInterface`
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return: None
        """
        storage = kwargs.get('storage', None)

        if storage is not None:
            self.__storage = self.verify_storage(storage)

        else:
            self.__storage = self.verify_storage(ProtocolStorage())

        super(BaseProtocolActionsImplementor, self).__init__()

    def to_tdo(self, in_data):

        """
        this methis will prepare a dynamic structure from the exist one, based on
        user request

        :param in_data:
        :return:
        """

        def inner(apidata, indata):
            """

            :param apidata:
            :type apidata: dprotocol instance
            :param indata:
            :type indata: iterable
            :param deep: how deep I'm

            :return: dict
            """

            # apidata is a dprotocol instance, predefined inside our backend as
            # DProtocol implementation in both way it inherit from BaseProtocolActions which provides
            # IBaseProtocolActionsInterface

            for key, _ in apidata.to_dict().iteritems():

                # so if we meet attribute from IBaseProtocolActionsInterface type means it's a sub protocol
                # and we have to call inner
                if IBaseProtocolActionsInterface.providedBy(getattr(apidata, key)):
                    inner(getattr(apidata, key), indata)

                else:

                    # otherwise we will looping over all items in indata
                    for inner_key, inner_val in indata.iteritems():

                        # 1. we checking whether the inner_key exist directly in our root dict of apidata
                        if inner_key in apidata.to_dict():

                            # if exist we get the value from apidata.to_dict().get(inner_key) with ik as key
                            indata[inner_key] = apidata.to_dict().get(inner_key)

                        elif isinstance(inner_val, dict):

                            # 2.if inner_val is a dict first we will trying to get the apidata key
                            # from this dict

                            if key in inner_val:

                                # if exist will update the indata for this key
                                indata[inner_key].update({key: apidata.to_dict().get(key)})

                            else:

                                # else we pass the inner_val to our inner again for more
                                # nested structures
                                inner(apidata, inner_val)
            return indata

        result = inner(self, in_data)

        return result

    def save(self):
        """

        :return:
        """

        try:

            if self.id is None:

                raise ValueError('The session id is not assigned')

        except AttributeError:

            raise NotImplementedError('the storage methods works only with protocols which provide a id attribute')

        self.add_session(id=self.id, session=self)
        return True

    def finish(self):

        """
        The session will be finished
        :return: False if session does not exist or self on success

        """
        return False if not self.__storage.session.pop(self.id, False) else self

    def get_child(self, child_members, in_dict):

        """

        :param child_members:
        :param in_dict:
        :return:

        """

        child_object = getattr(self, child_members)

        if not isinstance(child_object, BaseProtocolActionsImplementor):
            setattr(self, child_members, in_dict[child_members])

        else:

            self.to_object(
                in_dict=in_dict.get(child_members),
                in_obj=child_object
            )

    def to_object(self, in_dict=None, in_obj=None):

        """

        :param in_dict:
        :param in_obj:
        :return:
        """

        if in_dict is None:
            return False

        if in_obj is not None:
            self = in_obj

        for members, members_value in in_dict.iteritems():

            if isinstance(members_value, dict) or isinstance(members_value, BaseProtocolActionsImplementor):

                self.get_child(members, in_dict)

            else:

                if members == '_BaseProtocolActionsImplementor__storage':
                    continue

                setattr(self, members, members_value)

        return self

    @staticmethod
    def nice_name(in_name):

        """
        Will produce from "__attribute" -> "attribute"

        :param in_name:
        :type in_name: str

        :return: str

        """

        _, result = in_name.rsplit('__')
        return result

    def to_dict(self, dob=None):

        """

        :param dob:
        :return:
        """

        temp = {}

        if dob is not None:
            self = dob

        for members in self.__dict__:

            if members == '_BaseProtocolActionsImplementor__storage':
                continue

            if isinstance(self.__dict__[members], BaseProtocolActionsImplementor) is True:
                temp[self.nice_name(members)] = self.to_dict(dob=self.__dict__[members])

            else:

                # here we cover a case when we have a list and inside this list
                # we have members from IBaseProtocolActionsInterface
                # and convert all members to dict
                # this is not usual case and to_object will not work

                if isinstance(self.__dict__[members], list):
                    tmp = []

                    for mem in self.__dict__[members]:

                        if isinstance(mem, BaseProtocolActionsImplementor) is True:
                            tmp.append(mem.to_dict())

                    if tmp:
                        temp[self.nice_name(members)] = tmp

                    else:
                        temp[self.nice_name(members)] = self.__dict__[members]

                else:
                    temp[self.nice_name(members)] = self.__dict__[members]

        return temp

    def to_json(self, **kwargs):
        """

        :param indent:
        :return:
        """
        indent = kwargs.get('indent', None)

        if indent is not None and isinstance(indent, int):
            return json.dumps(self.to_dict(), indent=indent)

        else:
            return json.dumps(self.to_dict())

    def to_xml(self, in_dict=None):

        """

        Convert dict to xml

        :param in_dict:

        :return: xml
        """

        try:

            xml = xmltodict.unparse(in_dict or self.to_dict())

        except ValueError as error:
            raise ValueError(error.message)

        else:
            return xml

    def get_session(self, **kwargs):

        """

        :param kwargs:
        :return:
        """

        if 'id' in kwargs and kwargs.get('id'):
            return self.__storage.session.pop(kwargs.get('id'), False)

        else:
            raise AttributeError('Incorrect configure, the id is a required argument')

    def add_session(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        if 'id' in kwargs and 'session' in kwargs:

            _id = kwargs.get('id')

            if _id in self.__storage.session:
                return False

            session = kwargs.get('session')

            if isinstance(session, BaseProtocolActionsImplementor) is not True:
                __msg = 'Incorrect configure, you must pass a DProtocol implementation as session argument'
                raise AttributeError(__msg)

            self.__storage.session[_id] = session

            return self

        else:
            raise AttributeError('Incorrect configure, the id and a session are required arguments')

    def get_storage(self):

        """

        :return:
        """
        return self.__storage.session

    def flush_storage(self):

        """

        :return:
        """
        self.__storage.session = {}

    @staticmethod
    def verify_storage(storage):

        """

        :param storage:
        :return:
        """
        if not IProtocolStogareInterface.providedBy(storage):

            raise DoesNotImplement(
                'A storage {} does not implement IProtocolStogareInterface'.format(storage)
            )

        else:
            return storage

    @staticmethod
    def public_setter(kwargs, service):
        """

        :param kwargs:
        :param service:
        :return:
        """
        # get all attributes
        keys = kwargs.keys()

        # loop over them
        for k in keys:

            search_key = '_{}__{}'.format(service.__class__.__name__, k)

            # if these attribute are into this service dict
            if search_key in service.__dict__:
                # set it
                setattr(service, k, kwargs[k])

            else:
                raise AttributeError('Incorrect configure for {}, key: {}'.format(service, k))

        # if user are passed correct service attributes, they are set
        # otherwise just return requested service without changes
        return service

    # original from http://www.saltycrane.com/blog/2011/10/some-more-python-recursion-examples/
    # modified by dimd
    def get_all_keys(self, data=None):

        """
        This function gets all keys from dict recursively
        :param data:
        :type data: dict

        :return: list of keys
        """

        data = data or self.to_dict()

        keys = []

        def inner(data_):

            """

            Inner recursion
            :param data_:
            :return:

            """

            if isinstance(data_, dict):

                for key, value in data_.iteritems():

                    if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):

                        keys.append(key)
                        inner(value)

                    else:
                        keys.append(key)

            # elif isinstance(data_, list) or isinstance(data_, tuple):
            #     for item in data_:
            #         inner(item)

        inner(data)
        return keys
