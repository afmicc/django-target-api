from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import MessageFactory, RoomFactory
from applications.chats.models import Room
from applications.users.tests.factories import UserFactory


class RoomListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('room-list')

    def setUp(self):
        self.user = UserFactory(confirmed=True)

    def call_rooms_list(self):
        return self.client.get(self.url)

    def create_rooms(self, users, user=None):
        return [
            RoomFactory(members=[user or self.user, users[i]]) for i in range(len(users))
        ]

    def test_no_created_rooms_return_empty(self):
        self.client.force_authenticate(user=self.user)
        response = self.call_rooms_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_created_rooms_returns_room_and_receiver(self):
        rooms_count = 3
        receivers = UserFactory.create_batch(size=rooms_count)
        self.create_rooms(receivers)

        self.client.force_authenticate(user=self.user)
        response = self.call_rooms_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), rooms_count)
        self.assertEqual(len(response.data.get('results')), rooms_count)
        self.assertEqual(
            [key for key in response.json()['results'][0]],
            ['id', 'topic', 'receiver', 'unread_message_count', 'created_at'],
        )
        self.assertEqual(
            [key for key in response.json()['results'][0]['receiver']],
            ['id', 'email', 'name', 'gender', 'picture', ]
        )

    def test_created_room_returns_room_unread_message_count(self):
        receiver = UserFactory(confirmed=True)
        room = RoomFactory(members=[receiver, self.user])
        message_count = 3
        for value in [True, False]:
            MessageFactory.create_batch(
                message_count,
                room=room,
                writer=receiver,
                is_read=value
            )

        self.client.force_authenticate(user=self.user)
        response = self.call_rooms_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(len(response.data.get('results')), 1)
        room_responsed = response.json()['results'][0]
        self.assertEqual(
            room_responsed['unread_message_count'],
            message_count
        )

    def test_no_included_as_memeber_created_room_return_only_user_rooms(self):
        rooms_count = 3
        receivers = UserFactory.create_batch(size=rooms_count)
        user_rooms = self.create_rooms(receivers)
        other_receivers = UserFactory.create_batch(size=rooms_count)
        other_user = UserFactory(confirmed=True)
        self.create_rooms(other_receivers, other_user)

        self.assertEqual(Room.objects.count(), rooms_count * 2)

        self.client.force_authenticate(user=self.user)
        response = self.call_rooms_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), rooms_count)
        self.assertEqual(
            [r['id'] for r in response.json()['results']],
            [r.id for r in user_rooms]
        )
        self.assertEqual(
            [r['receiver']['id'] for r in response.json()['results']],
            [u.id for u in receivers]
        )
