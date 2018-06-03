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
        message = event['message']
        print("Send: %s" % message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'type': 'kookoo',
            'show': 'popup'
        }))
