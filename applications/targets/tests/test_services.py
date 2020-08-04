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
        'applications.notifications.services.NotificationCreator.create',
        return_value=None
    )
    def test_targets_do_not_create_notificaitons(self, notificator):
        self.call_matching_service()

        notificator.assert_not_called()

    @mock.patch(
        'applications.notifications.services.NotificationCreator.create',
        return_value=None
    )
    def test_compatible_targets_create_notificaitons(self, notificator):
        matching_target = factories.compatible_in_radius_target(self.topic)
        matching_target2 = factories.compatible_in_radius_target2(self.topic)

        self.call_matching_service()

        self.assertEqual(notificator.call_count, 4)

        calls = [
            mock.call(
                matching_target.owner,
                {'target_id': self.target.id},
                'You have a new match',
                f'A {self.target.topic.name} target is near you: {self.target.title}',
            ),
            mock.call(
                matching_target2.owner,
                {'target_id': self.target.id},
                'You have a new match',
                f'A {self.target.topic.name} target is near you: {self.target.title}',
            ),
            mock.call(
                self.user,
                {'target_id': matching_target.id},
                'You have a new match',
                f'A {matching_target.topic.name} target is near you: {matching_target.title}',
            ),
            mock.call(
                self.user,
                {'target_id': matching_target2.id},
                'You have a new match',
                f'A {matching_target2.topic.name} target is near you: {matching_target2.title}',
            ),
        ]
        notificator.assert_has_calls(calls, any_order=True)

    @mock.patch(
        'applications.notifications.services.NotificationCreator.create',
        return_value=None
    )
    def test_no_compatible_targets_do_not_create_notificaitons(self, notificator):
        other_topic = factories.TopicFactory()
        factories.incompatible_in_radius_target(other_topic)
        factories.compatible_out_radius_target(self.topic)

        self.call_matching_service()

        notificator.assert_not_called()
