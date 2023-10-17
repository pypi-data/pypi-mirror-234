# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.urls import re_path
from django.core.asgi import get_asgi_application
from django.utils.functional import LazyObject

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter

from lino.core.auth import get_user
from lino.modlib.notify.consumers import ClientConsumer

from .utils import LINOD
from .consumers import LinodConsumer


class UserLazyObject(LazyObject):
    """
    Throw a more useful error message when scope['user'] is accessed before it's resolved
    """

    def _setup(self):
        raise ValueError("Accessing scope user before it is ready.")


websocket_urlpatterns = []
WORKERS = dict()
websocket_urlpatterns.append(re_path(r"^WS/$", ClientConsumer.as_asgi()))
WORKERS[LINOD] = LinodConsumer.as_asgi()

async def _get_user(scope):
    class Wrapper:
        def __init__(self, session):
            self.session = session

    r = Wrapper(scope['session'])
    return await database_sync_to_async(get_user)(r)

class AuthMiddleware(BaseMiddleware):
    def populate_scope(self, scope):
        # Make sure we have a session
        if "session" not in scope:
            raise ValueError(
                "AuthMiddleware cannot find session in scope. SessionMiddleware must be above it."
            )
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await _get_user(scope)

    async def __call__(self, scope, receive=None, send=None):
        self.populate_scope(scope)
        await self.resolve_scope(scope)
        return await self.inner(scope, receive, send)


protos = dict(
    websocket = SessionMiddlewareStack(AuthMiddleware(URLRouter(websocket_urlpatterns))),
    channel = ChannelNameRouter(WORKERS)
)

protos.update(http=get_asgi_application())

application = ProtocolTypeRouter(protos)
