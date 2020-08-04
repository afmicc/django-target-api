from django.test import TestCase

from . import factories
from applications.users.tests.factories import UserFactory


class TopicModelTests(TestCase):
    def setUp(self):
        self.topic = factories.TopicFactory()

    def test_to_string_displays_name(self):
        self.assertEqual(self.topic.name, str(self.topic))


class TargetModelTests(TestCase):
    def test_to_string_displays_title(self):
        target = factories.TargetFactory()

        self.assertEqual(target.title, str(target))

    def test_only_one_target_compatible_query_return_empty(self):
        target = factories.TargetFactory()

        self.assertEqual(target.compatible_query().count(), 0)

    def test_same_user_targets_compatible_query_return_empty(self):
        user = UserFactory()
        topic = factories.TopicFactory()
        targets = factories.TargetFactory.create_batch(size=3, owner=user, topic=topic)
        target = targets[0]

        self.assertEqual(target.compatible_query().count(), 0)

    def test_matching_targets_compatible_query_return_coincidenses(self):
        user = UserFactory()
        topic = factories.TopicFactory()
        other_topic = factories.TopicFactory()
        target = factories.default_target(user, topic)

        matching_targets = [
            factories.compatible_in_radius_target(topic),
            factories.compatible_in_radius_target2(topic)
        ]
        unmatching_targets = [
            factories.incompatible_in_radius_target(other_topic),
            factories.compatible_out_radius_target(topic)
        ]

        self.assertEqual(target.compatible_query().count(), len(matching_targets))
        self.assertNotIn(
            unmatching_targets[0].id,
            target.compatible_query().values_list('id', flat=True)
        )
        self.assertNotIn(
            unmatching_targets[1].id,
            target.compatible_query().values_list('id', flat=True)
        )
