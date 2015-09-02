__author__ = 'dimd'

from zope.component import adapts

from ...factories.moderator import IModeratorFactory
from ...factories.user import IUserFactory
from ...factories.admin import IAdminFactory

from NetCatKS.Components import DefaultAdapter


class AdminModeratorSessionAdapter(DefaultAdapter):
    adapts(IAdminFactory, IModeratorFactory, IUserFactory)

__all__ = ['AdminModeratorSessionAdapter']