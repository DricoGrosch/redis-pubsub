from threading import Thread

from asgiref.sync import async_to_sync
from django.shortcuts import render
from django_redis_example.wsgi import _redis
def check_messages(room_name,subscriber):
    while True:
        message = subscriber.get_message()
        if message and not message['data'] == 1:
            try:
                message = message['data'].decode('utf-8')
                from channels.layers import get_channel_layer
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.send)(room_name, {"type": "chat_message",'message':message})
            except Exception as e:
                pass



def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    subscriber = _redis.pubsub()
    subscriber.subscribe(room_name)
    Thread(target=check_messages,args=[room_name,subscriber]).start()
    return render(request, 'room.html', {
        'room_name': room_name
    })
