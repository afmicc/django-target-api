from django.test import TestCase

from .factories import ContactFactory


class ContactModelTests(TestCase):
    def setUp(self):
        self.contact = ContactFactory()

    def test_to_string_displays_email(self):
        self.assertEqual(self.contact.email, str(self.contact))
