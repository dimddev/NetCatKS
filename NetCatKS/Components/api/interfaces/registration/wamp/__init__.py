__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IWAMPRegister(Interface):

    def register_wamp():
        """
        Registering of all objects which ends with Wamp prefix and are located inside component/wamp directory
        :return:
        """


class IWAMPResource(Interface):
    """
    marker
    """


class IWAMPComponent(Interface):

    def set_session(session):
        """
        register session to self.session
        :param session: Wamp Session
        :return:
        """