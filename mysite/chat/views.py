import json

from aioredis import Channel
from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework.response import Response
from rest_framework.views import APIView
from twisted.words.service import Group


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, slug):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(slug))
    })


class Record(APIView):
    def get(self, request, channel_name):
        # Send message to room group
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        print(channel_layer.group_send)
        from asgiref.sync import async_to_sync

        async_to_sync(channel_layer.group_send)("chat_%s" % channel_name, {
                'type': 'chat_messages',
                'message': "working........"
            })

        return Response({"test": "working..."})
