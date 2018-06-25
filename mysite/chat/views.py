import json
from xml.dom import minidom
from xml.etree import ElementTree

from aioredis import Channel
from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from twisted.words.service import Group

from .models import Record


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, slug):
    from random import randint

    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    import xml.etree.ElementTree as ET
    # create the file structure
    data = ET.Element('response')
    items = ET.SubElement(data, 'record')
    items.set('format', 'wav')
    items.set('silence', '3')
    items.set('maxduration', '30')
    items.text = '%s' % random_with_N_digits(7)

    # item1 = ET.SubElement(items, 'item')
    # item2 = ET.SubElement(items, 'item')
    # item1.set('name', 'item1')
    # item2.set('name', 'item2')
    # item1.text = 'item1abc'
    # item2.text = 'item2abc'

    # create a new XML file with the results
    mydata = ET.tostring(data)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(slug)),
        'kookoo_xml': mydata
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


class REDView(APIView):
    def post(self, request):
        # Send message to room group
        print(request.POST)
        print(request.POST.get('phone_no'))
        print(request.POST.get('status'))
        print(request.POST.get('sid'))
        print(request.POST.get('caller_id'))
        print(request.POST.get('duration'))
        print(request.POST.get('telco_code'))

        return Response({"test": "working..."})


class AlexaView(APIView):
    def get(self, request):
        response = {
            "company": "raunakgroup",
            "current_campaign": "subse sasta ghar",
            "total_lead": "50"
        }

        return Response(response, status=status.HTTP_200_OK)

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

        if request.GET.get('event', None) == 'Dial' or request.GET.get('event', None) == 'Hangup':
            return render(request, 'chat/hangup.html', context={'file_name': random_with_N_digits(7)})

        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        print(channel_layer.group_send)
        from asgiref.sync import async_to_sync

        async_to_sync(channel_layer.group_send)("chat_soham", {
            'type': 'chat_messages',
            'sid': request.GET.get('sid', None),
            'event': request.GET.get('event', None),
            'cid': request.GET.get('cid', None),
            'call_member': request.GET.get('called_number', None),
            'request_time': request.GET.get('request_time', None),
            'circle': request.GET.get('circle', None),
            'operator': request.GET.get('operator', None),
            'cid_type': request.GET.get('cid_type', None),
            'cid_e164': request.GET.get('cid_e164', None),
            'cid_country': request.GET.get('cid_country', None),
            'total_call_duration': request.GET.get('total_call_duration', None),
            'data': request.GET.get('data', None),
            'status': request.GET.get('status', None),
            'rec_md5_checksum': request.GET.get('rec_md5_checksum', None),
            'record_duration': request.GET.get('record_duration', None),
            'called_number': request.GET.get('called_number', None)
        })
        #
        # import xml.etree.ElementTree as ET
        # # create the file structure
        # data = ET.Element('response')
        # items = ET.SubElement(data, 'record')
        # items.set('format', 'wav')
        # items.set('silence', '3')
        # items.set('maxduration', '30')
        # items.text = '%s' % random_with_N_digits(7)
        #
        # # item1 = ET.SubElement(items, 'item')
        # # item2 = ET.SubElement(items, 'item')
        # # item1.set('name', 'item1')
        # # item2.set('name', 'item2')
        # # item1.text = 'item1abc'
        # # item2.text = 'item2abc'
        # mydata = ET.tostring(data)


        # import xml.dom.minidom
        # xml = xml.dom.minidom.parseString(mydata)  # or xml.dom.minidom.parseString(xml_string)
        # pretty_xml_as_string = xml.toprettyxml()

        # rough_string = ElementTree.tostring(data, 'utf-8')
        # reparsed = minidom.parseString(rough_string)
        # mydata = reparsed.toprettyxml(indent="\t")

        # if request.GET.get('event', None) == 'Hangup':
        #      # TODO: Send Message:
        #      response = requests.get("http://www.kookoo.in/outbound/outbound_sms.php?api_key=%s&phone_no=%s&message=%s" %
        #                              ("KKfc447077bf57589e5f92b23ffb219982", request.GET.get('cid_e164', None), "Thank you for call the kookoo"))
        #      print(response.status_code)
        #      print(response.content)
        print("Inserted successfully")

        return render(request, 'chat/record.html', context={'file_name': random_with_N_digits(7)})
