# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.home.routing import websocket_urlpatterns 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Manejo de protocolo HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Tus rutas WebSocket definidas en 'routing.py'
        )
    ),
})
