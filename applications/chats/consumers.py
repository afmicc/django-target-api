from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        room_id = self.scope['url_route']['kwargs']['room']
        self.room = await self._get_room(self.user, room_id)
        self.room_group_name = f'chat_room_{room_id}'

        if self.user.is_authenticated and self.room:
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
    def _get_room(self, user, room_id):
        return user.room_set.get(id=room_id)

    @database_sync_to_async
    def _save_message(self, user, room, message):
        return room.message_set.create(writer=user, content=message)
