import json

from aioredis import Channel
from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from twisted.words.service import Group

from .models import Record


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, slug):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(slug))
    })


class RecordAPIView(APIView):
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


class VoiceRecordTemplate(TemplateView):
    def get(self, request, **kwargs):
        # print("Event is: %s" % request.GET)

        from random import randint

        def random_with_N_digits(n):
            range_start = 10 ** (n - 1)
            range_end = (10 ** n) - 1
            return randint(range_start, range_end)

        _record = Record(
            event=request.GET.get('event', None),
            sid=request.GET.get('sid', None),
            cid=request.GET.get('cid', None),
            call_member=request.GET.get('called_number', None),
            request_time=request.GET.get('request_time', None),
            circle=request.GET.get('circle', None),
            operator=request.GET.get('operator', None),
            cid_type=request.GET.get('cid_type', None),
            cid_e164=request.GET.get('cid_e164', None),
            cid_country=request.GET.get('cid_country', None),
            total_call_duration=request.GET.get('total_call_duration', None),
            data=request.GET.get('data', None),
            status=request.GET.get('status', None),
            rec_md5_checksum=request.GET.get('rec_md5_checksum', None),
            record_duration=request.GET.get('record_duration', None),
            called_number=request.GET.get('called_number', None),
        )
        _record.save()

        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        print(channel_layer.group_send)
        from asgiref.sync import async_to_sync

        async_to_sync(channel_layer.group_send)("chat_soham", {
            'type': 'chat_messages',
            'message': request.GET.get('sid', None)
        })

        # if request.GET.get('event', None) == 'Hangup':
        #      # TODO: Send Message:
        #      response = requests.get("http://www.kookoo.in/outbound/outbound_sms.php?api_key=%s&phone_no=%s&message=%s" %
        #                              ("KKfc447077bf57589e5f92b23ffb219982", request.GET.get('cid_e164', None), "Thank you for call the kookoo"))
        #      print(response.status_code)
        #      print(response.content)
        print("Inserted successfully")

        return render(request, 'chat/record.html', context={'file_name': random_with_N_digits(7)})
