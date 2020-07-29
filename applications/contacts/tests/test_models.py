from django.test import TestCase

from .factories import ContactFactory


class UserModelTests(TestCase):
    def setUp(self):
        self.user = ContactFactory()

    def test_to_string_displays_email(self):
        self.assertEqual(self.user.email, str(self.user))
