import factory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import ContactFactory
from applications.contacts.models import Contact
from applications.users.tests.factories import UserFactory


class ContactCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('contact-list')

    def setUp(self):
        self.params = factory.build(dict, FACTORY_CLASS=ContactFactory,)

    def call_create_contact(self):
        return self.client.post(self.url, self.params)

    def test_all_params_valid_respond_success_and_data(self):
        response = self.call_create_contact()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(
            [key for key in response.json()],
            ['id', 'email', 'message', 'writer', ]
        )

    def test_all_params_valid_save_data(self):
        self.call_create_contact()

        last = Contact.objects.last()
        self.assertEqual(self.params['email'], last.email)
        self.assertEqual(self.params['message'], last.message)
        self.assertIsNone(last.writer)

    def test_missing_email_respond_failure(self):
        del self.params['email']

        response = self.call_create_contact()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_message_respond_failure(self):
        del self.params['message']

        response = self.call_create_contact()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_loged_user_respond_success_and_save_data(self):
        user = UserFactory(confirmed=True)
        self.client.force_authenticate(user=user)
        response = self.call_create_contact()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        last = Contact.objects.last()
        self.assertEqual(self.params['email'], last.email)
        self.assertEqual(self.params['message'], last.message)
        self.assertEqual(user, last.writer)
