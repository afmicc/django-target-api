from django.db.models import ObjectDoesNotExist
from django.test import override_settings

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from faker import Faker
from faker.providers import lorem
from rest_framework.authtoken.models import Token

from applications.chats.consumers import ChatConsumer
from applications.chats.tests.factories import RoomFactory
from applications.users.tests.factories import UserFactory
from target_api.middlewares import TokenAuthMiddlewareStack


fake = Faker()
fake.add_provider(lorem)


@database_sync_to_async
def login(user):
    token = Token.objects.create(user=user)
    return token.key


@database_sync_to_async
def create_room():
    user1 = UserFactory()
    user2 = UserFactory()
    room = RoomFactory(members=[user1, user2])
    return (room.id, user1, user2)


channel_layers_setting = {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}
}


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_send_and_recive_messages_successfully():
    with override_settings(CHANNEL_LAYERS=channel_layers_setting):
        room_id, user1, user2 = await create_room()

        token = await login(user1)
        communicator1 = WebsocketCommunicator(
            TokenAuthMiddlewareStack(ChatConsumer),
            f'/ws/chats/{room_id}/?token={token}',
        )
        communicator1.scope['url_route'] = {
            'args': (),
            'kwargs': {'room': room_id}
        }
        connected1, _ = await communicator1.connect()
        assert connected1

        token = await login(user2)
        communicator2 = WebsocketCommunicator(
            TokenAuthMiddlewareStack(ChatConsumer),
            f'/ws/chats/{room_id}/?token={token}',
        )
        communicator2.scope['url_route'] = {
            'args': (),
            'kwargs': {'room': room_id}
        }
        connected2, _ = await communicator2.connect()
        assert connected2

        message = fake.text(max_nb_chars=250)
        await communicator1.send_json_to({'message': message, })

        response = await communicator1.receive_json_from()
        assert response == {'message': message, 'user': user1.id, }
        response = await communicator2.receive_json_from()
        assert response == {'message': message, 'user': user1.id, }

        message = fake.text(max_nb_chars=250)
        await communicator2.send_json_to({'message': message, })

        response = await communicator1.receive_json_from()
        assert response == {'message': message, 'user': user2.id, }
        response = await communicator2.receive_json_from()
        assert response == {'message': message, 'user': user2.id, }

        await communicator1.disconnect()
        await communicator2.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_unauthorized_user_reject_conection():
    with override_settings(CHANNEL_LAYERS=channel_layers_setting):
        room_id, user1, _ = await create_room()

        await login(user1)
        communicator = WebsocketCommunicator(
            TokenAuthMiddlewareStack(ChatConsumer),
            f'/ws/chats/{room_id}/?token=fake-token',
        )
        communicator.scope['url_route'] = {
            'args': (),
            'kwargs': {'room': room_id}
        }

        connected, _ = await communicator.connect()
        assert not connected


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_not_found_room_reject_conection():
    with override_settings(CHANNEL_LAYERS=channel_layers_setting):
        with pytest.raises(ObjectDoesNotExist):
            room_id, user1, _ = await create_room()
            room_id *= 10

            token = await login(user1)
            communicator = WebsocketCommunicator(
                TokenAuthMiddlewareStack(ChatConsumer),
                f'/ws/chats/{room_id}/?token={token}',
            )
            communicator.scope['url_route'] = {
                'args': (),
                'kwargs': {'room': room_id}
            }

            connected, _ = await communicator.connect()
            assert not connected
