__author__ = 'dimd'

from zope.component import adapts
from ...factories.moderator import IModeratorFactory
from ...factories.user import IUserFactory

from NetCatKS.Components import DefaultAdapter


class ModeratorUserAdapter(DefaultAdapter):
    adapts(IModeratorFactory, IUserFactory)


__all__ = ['ModeratorUserAdapter']