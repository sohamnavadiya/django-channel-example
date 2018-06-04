from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('Room name: %s' % self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('Receive: %s' % message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_messages',
                'message': message
            }
        )

    async def chat_messages(self, event):
        sid=event['sid']
        _event=event['event']
        cid=event['cid']
        call_member=event['called_number']
        request_time=event['request_time']
        circle=event['circle']
        operator=event['operator']
        cid_type=event['cid_type']
        cid_e164=event['cid_e164']
        cid_country=event['cid_country']
        total_call_duration=event['total_call_duration']
        data=event['data']
        status=event['status']
        rec_md5_checksum=event['rec_md5_checksum']
        record_duration=event['record_duration']
        called_number=event['called_number']

        # print("Send: %s" % message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sid': sid,
            'event': _event,
            'cid': cid,
            'call_member': call_member,
            'request_time': request_time,
            'circle': circle,
            'operator': operator,
            'cid_type': cid_type,
            'cid_e164': cid_e164,
            'cid_country': cid_country,
            'total_call_duration': total_call_duration,
            'data': data,
            'status': status,
            'rec_md5_checksum': rec_md5_checksum,
            'record_duration': record_duration,
            'called_number': called_number
        }))
