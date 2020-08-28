from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import MessageFactory, RoomFactory
from applications.chats.models import Message
from applications.users.tests.factories import UserFactory


class MessagesSetLastMessageReadTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(confirmed=True)
        self.receiver = UserFactory(confirmed=True)
        self.room = RoomFactory(members=[self.user, self.receiver])

    def call_set_last_message_read(self, rooom, from_message):
        url = reverse(
            'message-set-last-message-read',
            kwargs={'room': rooom.id, 'pk': from_message.id},
        )
        return self.client.post(url)

    def test_only_received_messages_read_given_message(self):
        messages_count = 3
        messages = MessageFactory.create_batch(
            messages_count,
            room=self.room,
            writer=self.receiver
        )
        message_to_read = messages[0]

        self.client.force_authenticate(user=self.user)
        response = self.call_set_last_message_read(self.room, message_to_read)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        db_messages = Message.objects.all()
        self.assertEqual(db_messages[2].id, message_to_read.id)
        self.assertTrue(db_messages[2].is_read)
        self.assertFalse(db_messages[1].is_read)
        self.assertFalse(db_messages[0].is_read)

    def test_mixed_messages_read_given_message_and_previous(self):
        received_messages = MessageFactory.create_batch(
            2,
            room=self.room,
            writer=self.receiver
        )
        MessageFactory.create_batch(
            2,
            room=self.room,
            writer=self.user
        )
        received_messages += MessageFactory.create_batch(
            2,
            room=self.room,
            writer=self.receiver
        )

        message_to_read = received_messages[1]

        self.client.force_authenticate(user=self.user)
        response = self.call_set_last_message_read(self.room, message_to_read)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        db_messages = Message.objects.exclude(writer__id=self.user.id)
        self.assertEqual(db_messages[2].id, message_to_read.id)
        self.assertTrue(db_messages[2].is_read)
        self.assertTrue(db_messages[3].is_read)
        self.assertFalse(db_messages[1].is_read)
        self.assertFalse(db_messages[0].is_read)

        db_messages = Message.objects.filter(writer__id=self.user.id)
        self.assertFalse(db_messages[1].is_read)
        self.assertFalse(db_messages[0].is_read)

    def test_user_does_not_belong_to_room_respond_forbidden(self):
        room = RoomFactory(members=[UserFactory(confirmed=True), self.receiver])
        message_to_read = MessageFactory.create(
            room=room,
            writer=self.receiver
        )

        self.client.force_authenticate(user=self.user)
        response = self.call_set_last_message_read(room, message_to_read)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_does_not_belong_to_room_respond_not_found(self):
        room = RoomFactory(members=[UserFactory(confirmed=True), self.receiver])
        message_to_read = MessageFactory.create(
            room=room,
            writer=self.receiver
        )

        self.client.force_authenticate(user=self.user)
        response = self.call_set_last_message_read(self.room, message_to_read)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_logged_user_respond_unauthorized(self):
        message_to_read = MessageFactory.create(
            room=self.room,
            writer=self.receiver
        )

        response = self.call_set_last_message_read(self.room, message_to_read)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
