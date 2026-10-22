"""
ASGI config for codeduel project with Django Channels WebSocket support.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeduel.settings')

django_asgi_app = get_asgi_application()

import battles.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            battles.routing.websocket_urlpatterns
        )
    ),
})
