import asyncio
import functools
import json
import time

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.utils import await_many_dispatch
from django_redis_example.wsgi import _redis


class ChatConsumer(AsyncWebsocketConsumer):

    async def __call__(self, receive, send):
        self.channel_layer = get_channel_layer(self.channel_layer_alias)
        if self.channel_layer is not None:
            self.channel_name = self.scope['url_route']['kwargs']['room_name']
            self.channel_receive = functools.partial(
                self.channel_layer.receive, self.channel_name
            )
        if self._sync:
            self.base_send = async_to_sync(send)
        else:
            self.base_send = send
        try:
            if self.channel_layer is not None:
                await await_many_dispatch(
                    [receive, self.channel_receive], self.dispatch
                )
            else:
                await await_many_dispatch([receive], self.dispatch)
        except StopConsumer:
            pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        _redis.publish(self.channel_name, message)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
