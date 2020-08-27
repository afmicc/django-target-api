from django.utils.translation import gettext_lazy as _

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from applications.notifications.services import NotificationCreator


class ChatConsumer(AsyncJsonWebsocketConsumer):
    NOTIFICATION_TITLE = 'New message'
    NOTIFICATION_BODY = 'New message about {}'

    notificator = NotificationCreator()

    async def connect(self):
        self.user = self.scope['user']
        room_id = self.scope['url_route']['kwargs']['room']

        if self.user.is_authenticated:
            self.room, self.receiver, self.topic = await self._get_room_data(self.user, room_id)
            self.room_group_name = f'chat_room_{room_id}'

            if self.room:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()
        else:
            raise DenyConnection()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        message = content['message']
        if not message:
            return

        await self._save_message(self.user, self.room, message)
        await self._send_notification_to_receiver(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'data':  {
                    'message': message,
                    'user': self.user.id,
                }
            }
        )

    async def room_message(self, event):
        data = event['data']
        await self.send_json(content=data)

    @database_sync_to_async
    def _get_room_data(self, user, room_id):
        room = user.room_set.get(id=room_id)
        receiver = room.members.exclude(id=user.id).first()
        return (room, receiver, room.topic)

    @database_sync_to_async
    def _save_message(self, user, room, message):
        return room.message_set.create(writer=user, content=message)

    async def _send_notification_to_receiver(self, message):
        data = {'room_id': self.room.id}
        title = _(self.NOTIFICATION_TITLE)
        message = _(self.NOTIFICATION_BODY).format(self.topic.name)

        await self.notificator.create_async(self.receiver, data, title, message)
