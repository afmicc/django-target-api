from django.test import TestCase
import mock

from . import factories
from applications.targets.services import TargetMatchingService
from applications.users.tests.factories import UserFactory


class TargetMatchingServiceTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.topic = factories.TopicFactory()
        self.target = factories.default_target(self.user, self.topic)

    def call_matching_service(self):
        matching = TargetMatchingService()
        matching.process_target(self.target)

    @mock.patch(
        'applications.chats.services.RoomCreator.create_from_target_match',
        return_value=None
    )
    @mock.patch(
        'applications.notifications.services.NotificationCreator.create',
        return_value=None
    )
    def test_targets_do_not_create_notificaitons(self, notificator, room_creator):
        self.call_matching_service()

        notificator.assert_not_called()
        room_creator.assert_not_called()

    @mock.patch(
        'applications.chats.services.RoomCreator.create_from_target_match',
        return_value=None
    )
    @mock.patch(
        'applications.notifications.services.NotificationCreator.create',
        return_value=None
    )
    def test_compatible_targets_create_notificaitons(self, notificator, room_creator):
        matching_target = factories.compatible_in_radius_target(self.topic)
        matching_target2 = factories.compatible_in_radius_target2(self.topic)

        self.call_matching_service()

        self.assertEqual(notificator.call_count, 4)

        calls = [
            mock.call(
                matching_target.owner,
                {'target_id': self.target.id},
                TargetMatchingService.NOTIFICATION_TITLE,
                TargetMatchingService.NOTIFICATION_BODY.format(self.target.topic.name, self.target.title),
            ),
            mock.call(
                matching_target2.owner,
                {'target_id': self.target.id},
                TargetMatchingService.NOTIFICATION_TITLE,
                TargetMatchingService.NOTIFICATION_BODY.format(self.target.topic.name, self.target.title),
            ),
            mock.call(
                self.user,
                {'target_id': matching_target.id},
                TargetMatchingService.NOTIFICATION_TITLE,
                TargetMatchingService.NOTIFICATION_BODY.format(matching_target.topic.name, matching_target.title),
            ),
            mock.call(
                self.user,
                {'target_id': matching_target2.id},
                TargetMatchingService.NOTIFICATION_TITLE,
                TargetMatchingService.NOTIFICATION_BODY.format(matching_target2.topic.name, matching_target2.title),
            ),
        ]
        notificator.assert_has_calls(calls, any_order=True)

        calls = [
            mock.call(
                self.target,
                self.user,
                matching_target2.owner,
            ),
            mock.call(
                self.target,
                self.user,
                matching_target.owner,
            ),
        ]
        room_creator.assert_has_calls(calls, any_order=True)

    @mock.patch(
        'applications.chats.services.RoomCreator.create_from_target_match',
        return_value=None
    )
    @mock.patch(
        'applications.notifications.services.NotificationCreator.create',
        return_value=None
    )
    def test_no_compatible_targets_do_not_create_notificaitons(self, notificator, room_creator):
        other_topic = factories.TopicFactory()
        factories.incompatible_in_radius_target(other_topic)
        factories.compatible_out_radius_target(self.topic)

        self.call_matching_service()

        notificator.assert_not_called()
        room_creator.assert_not_called()
