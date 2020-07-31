from django.test import TestCase

from .factories import NotificationFactory


class NotificationModelTests(TestCase):
    def setUp(self):
        self.notification = NotificationFactory()

    def test_to_string_displays_email(self):
        self.assertEqual(
            f'{self.notification.title} - {self.notification.message}',
            str(self.notification)
        )
