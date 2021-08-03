# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_redis_example.settings')
application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [url('ws/chat/(?P<room_name>\w+)/$', ChatConsumer),]
    ),
})
