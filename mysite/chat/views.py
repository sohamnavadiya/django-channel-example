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
    def get(self, request):
        # Send message to room group
        return Response({"test": "working..."})
