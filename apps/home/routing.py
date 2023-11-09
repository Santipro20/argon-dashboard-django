from django.urls import re_path
from apps.home.consumers import MyConsumer

websocket_urlpatterns = [
    re_path(r"ws/co2_updates/$", MyConsumer.as_asgi()),
]
