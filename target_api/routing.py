from channels.routing import ProtocolTypeRouter, URLRouter

from .middlewares import TokenAuthMiddlewareStack
from applications.chats import routing as chats

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            chats.websocket_urlpatterns
        )
    ),
})
