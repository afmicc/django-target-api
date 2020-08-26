from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        params = self.scope['query_string'].decode('utf-8').split('=')
        self.scope['user'] = await self._get_user_by_query_param(*params)

        inner = self.inner(self.scope)
        return await inner(receive, send)

    @database_sync_to_async
    def _get_user_by_query_param(self, name, value):
        if name.lower() != 'token':
            raise ValueError(_('The token param is mandatory'))

        try:
            token = Token.objects.get(key=value)
            user = token.user
        except Token.DoesNotExist:
            user = AnonymousUser()
        return user


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
