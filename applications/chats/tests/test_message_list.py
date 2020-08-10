import random
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import MessageFactory, RoomFactory
from applications.users.tests.factories import UserFactory


class MessageListTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(confirmed=True)
        self.receiver = UserFactory(confirmed=True)
        self.room = RoomFactory(members=[self.user, self.receiver])

    def call_messages_list(self, rooom, page=1):
        url = reverse('message-list', kwargs={'room': rooom.id}) + f'?page={page}'
        return self.client.get(url)

    def create_messages(self, count=2):
        writers = [self.user, self.receiver]
        return [
            MessageFactory(room=self.room, writer=writers[random.randint(0, 1)]) for i in range(count)
        ]

    def test_no_messages_return_empty(self):
        self.client.force_authenticate(user=self.user)
        response = self.call_messages_list(self.room)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_created_messages_returns_messages_sorted(self):
        messages_count = 3
        messages = self.create_messages(messages_count)

        self.client.force_authenticate(user=self.user)
        response = self.call_messages_list(self.room)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), messages_count)
        self.assertEqual(len(response.data.get('results')), messages_count)
        self.assertEqual(
            [key for key in response.json()['results'][0]],
            ['content', 'room', 'writer', 'created_at', ]
        )

        messages.sort(key=(lambda x: x.created_at), reverse=True)
        response_data = [
            {
                'content': m.content,
                'room': m.room.id,
                'writer': m.writer.name,
                'created_at': m.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            } for m in messages
        ]
        self.assertEqual(
            response.json()['results'],
            response_data
        )

    def test_no_included_as_memeber_created_room_respond_forbidden(self):
        self.create_messages()

        room = RoomFactory(members=[UserFactory(confirmed=True), self.receiver])

        self.client.force_authenticate(user=self.user)
        response = self.call_messages_list(room)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_loged_user_respond_unauthorized(self):
        self.create_messages()

        response = self.call_messages_list(self.room)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_created_messages_returns_messages_paged(self):
        page_size_1 = 10
        page_size_2 = 7
        messages_count = page_size_1 + page_size_2
        self.create_messages(messages_count)

        self.client.force_authenticate(user=self.user)
        response = self.call_messages_list(self.room)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), messages_count)
        self.assertEqual(len(response.data.get('results')), page_size_1)

        response = self.call_messages_list(self.room, 2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), messages_count)
        self.assertEqual(len(response.data.get('results')), page_size_2)
