__author__ = 'dimd'
import json
import xmltodict
from zope.interface import implementer
from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement


from NetCatKS.DProtocol.api.interfaces.actions import IBaseProtocolActionsInterface
from NetCatKS.DProtocol.api.interfaces.storage import IProtocolStogareInterface
from NetCatKS.DProtocol.api.interfaces.dymanic import IDynamicProtocolInterface
from NetCatKS.DProtocol.api.public.storage import ProtocolStorage
from NetCatKS.DProtocol.api.implementors.filters import ProtocolFiltersImplementor


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

    def save(self):
        """

        :return:
        """
        if self.id is None:
            raise AttributeError('The session id is not assigned')

        self.add_session(id=self.id, session=self)
        return True

    def finish(self):

        """

        :return:
        """
        try:
            self.__storage.session.pop(self.id)

        except KeyError:
            return False

        else:
            return self

    def to_object(self, in_dict=None, in_obj=None, **kwargs):

        """

        :param in_dict:
        :param in_obj:
        :return:
        """
        if in_dict is None:
            return False

        if in_obj is not None:
            self = in_obj

        def get_child(child_members, in_dict):

            child_object = getattr(self, child_members)

            try:

                verifyObject(IBaseProtocolActionsInterface, child_object)

            except DoesNotImplement:
                # set up child
                setattr(self, child_members, in_dict[child_members])

            else:

                self.to_object(
                    in_dict=in_dict.get(child_members),
                    in_obj=child_object
                )

        for members in in_dict.keys():

            if type(in_dict[members]) is dict or IBaseProtocolActionsInterface.providedBy(in_dict[members]):
                get_child(members, in_dict)

            else:

                if members == '_BaseProtocolActionsImplementor__storage':
                    continue

                try:
                    setattr(self, members, in_dict[members])

                except AttributeError as e:
                    print 'MEMBERS {}, DICT {} {}'.format(members, in_dict[members], e.message)

        return self

    def to_dict(self, dob=None):

        """

        :param dob:
        :return:
        """

        temp = {}

        if dob is not None:
            self = dob

        def nice_name(in_name):
            temp, result = in_name.rsplit('__')
            return result

        for members in self.__dict__:

            if members == '_BaseProtocolActionsImplementor__storage':
                continue

            if IBaseProtocolActionsInterface.providedBy(self.__dict__[members]) is True:

                temp[nice_name(members)] = self.to_dict(dob=self.__dict__[members])

            else:

                # here we cover a case when we have a list and inside this list
                # we have members from IBaseProtocolActionsInterface
                # and convert all members to dict
                # this is not usual case and to_object will not work

                if isinstance(self.__dict__[members], list):

                    tmp = []

                    for mem in self.__dict__[members]:

                        if IBaseProtocolActionsInterface.providedBy(mem):
                            # print 1111
                            # print mem.to_dict()
                            tmp.append(mem.to_dict())

                    if tmp:

                        temp[nice_name(members)] = tmp

                    else:

                        temp[nice_name(members)] = self.__dict__[members]

                else:

                    temp[nice_name(members)] = self.__dict__[members]

        return temp

    def to_json(self, **kwargs):
        """

        :param indent:
        :return:
        """
        indent = kwargs.get('indent', None)

        if indent is not None and type(indent) is int:
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

            return xmltodict.unparse(in_dict or self.to_dict())

        except Exception as e:
            print e.message

    def get_session(self, **kwargs):

        """

        :param kwargs:
        :return:
        """

        if 'id' in kwargs and kwargs['id']:

            try:

                session = self.__storage.session.pop(kwargs.get('id'), False)

            except KeyError as e:

                print('TICKET WITH ID {} DOES NOT EXIST IN TICKET STORAGE'.format(e))
                return False

            else:

                return session

        else:

            return False

    def add_session(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        if 'id' in kwargs and 'session' in kwargs:

            if kwargs.get('id') in self.__storage.session:
                return False

            try:

                session = kwargs.get('session')

                if not IDynamicProtocolInterface.providedBy(session):
                    raise Exception('Incorrect configure, you must pass DProtocol implementation as session argument')

                self.__storage.session[kwargs.get('id')] = kwargs.get('session')

            except Exception as e:
                print e.message
                return False

            else:
                return self

        else:

            raise AttributeError('Incorrect configure, id and session are required argument')

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

    def verify_storage(self, storage):

        """

        :param storage:
        :return:
        """
        try:
            verifyObject(IProtocolStogareInterface, storage)

        except DoesNotImplement as e:
            print e

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
                raise Exception('Incorrect configure for {}, key: {}'.format(service, k))

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

        def inner(data):

            if isinstance(data, dict):

                for k, v in data.iteritems():
                    if (isinstance(v, dict) or
                        isinstance(v, list) or
                        isinstance(v, tuple)
                        ):
                        keys.append(k)
                        inner(v)
                    else:
                        keys.append(k)

            elif isinstance(data, list) or isinstance(data, tuple):
                for item in data:
                    inner(item)

        inner(data)
        return keys