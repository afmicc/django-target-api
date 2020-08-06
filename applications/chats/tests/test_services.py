from django.core.exceptions import ValidationError
from django.test import TestCase

from applications.chats.services import RoomCreator
from applications.chats.models import Room
from applications.chats.tests.factories import RoomFactory
from applications.targets.tests.factories import TargetFactory, TopicFactory
from applications.users.tests.factories import UserFactory


class TestRoomCreator(TestCase):
    def setUp(self):
        self.member_one = UserFactory()
        self.member_two = UserFactory()
        topic = TopicFactory()
        self.target = TargetFactory(owner=self.member_one, topic=topic)
        self.target = TargetFactory(owner=self.member_two, topic=topic)

    def call_create_from_target_match(self, *members):
        RoomCreator().create_from_target_match(self.target, *members)

    def test_create_room_with_two_members_successfully(self):
        self.call_create_from_target_match(self.member_one, self.member_two)

        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(
            Room.objects.filter(members__id=self.member_one.id, topic=self.target.topic).count(),
            1
        )
        self.assertEqual(
            Room.objects.filter(members__id=self.member_two.id, topic=self.target.topic).count(),
            1
        )

    def test_create_room_with_three_members_fail(self):
        new_user = UserFactory()

        with self.assertRaises(ValidationError) as error:
            self.call_create_from_target_match(self.member_one, self.member_two, new_user)

        self.assertIsNotNone(error)
        self.assertDictEqual(
            error.exception.message_dict,
            {'members': ['You can‘t create a room with more than two members']}
        )
        self.assertEqual(Room.objects.count(), 0)
        self.assertEqual(
            Room.objects.filter(members__id=self.member_one.id, topic=self.target.topic).count(),
            0
        )
        self.assertEqual(
            Room.objects.filter(members__id=self.member_two.id, topic=self.target.topic).count(),
            0
        )
        self.assertEqual(
            Room.objects.filter(members__id=new_user.id, topic=self.target.topic).count(),
            0
        )

    def test_create_room_with_one_members_fail(self):
        with self.assertRaises(ValidationError) as error:
            self.call_create_from_target_match(self.member_one)

        self.assertIsNotNone(error)
        self.assertDictEqual(
            error.exception.message_dict,
            {'members': ['You must create a room with two members']}
        )
        self.assertEqual(Room.objects.count(), 0)
        self.assertEqual(
            Room.objects.filter(members__id=self.member_one.id, topic=self.target.topic).count(),
            0
        )

    def test_create_room_replicating_ignore(self):
        RoomFactory(members=[self.member_one, self.member_two], topic=self.target.topic)
        self.assertEqual(Room.objects.count(), 1)

        self.call_create_from_target_match(self.member_one, self.member_two)

        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(
            Room.objects.filter(members__id=self.member_one.id, topic=self.target.topic).count(),
            1
        )
        self.assertEqual(
            Room.objects.filter(members__id=self.member_two.id, topic=self.target.topic).count(),
            1
        )
