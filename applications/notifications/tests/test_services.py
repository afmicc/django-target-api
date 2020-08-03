from django.test import TestCase
import factory
from faker import Faker
import mock

from applications.notifications.models import Notification
from applications.notifications.services import NotificationCreator, NotificationSender
from applications.users.tests.factories import UserFactory
from applications.notifications.tests.factories import NotificationFactory

fake = Faker()


class TestNotificationCreator(TestCase):
    def setUp(self):
        self.user = UserFactory(confirmed=True)
        params = factory.build(dict, FACTORY_CLASS=NotificationFactory, user=None,)
        self.title = params['title']
        self.message = params['message']
        self.data = {'id': fake.random_number()}

    @mock.patch(
        'applications.notifications.services.NotificationSender.send_notification',
        return_value=None
    )
    def test_send_notification_successfully_store_notificaiton(self, send_notification):
        creator = NotificationCreator()
        creator.create(self.user, self.data, self.title, self.message)

        self.assertEqual(send_notification.call_count, 1)

        last = Notification.objects.filter(user=self.user).last()
        self.assertEqual(self.user, last.user)
        self.assertEqual(self.message, last.message)

    @mock.patch(
        'applications.notifications.services.NotificationSender.send_notification',
        side_effect=Exception
    )
    def test_send_notification_raise_exception_do_not_store_notificaiton(self, send_notification):
        with self.assertRaises(Exception):
            creator = NotificationCreator()
            creator.create(self.user, self.data, self.title, self.message)

            self.assertEqual(send_notification.call_count, 1)

            last = Notification.objects.filter(user=self.user).last()
            self.assertIsNone(last)


class TestNotificationSender(TestCase):
    def setUp(self):
        self.emails = [fake.email()] * 5
        self.data = {'id': fake.random_number()}
        self.message = fake.text(max_nb_chars=50)

    @mock.patch(
        'onesignal_sdk.client.Client.send_notification',
        return_value=None
    )
    def test_one_email_param_call_provider_with_valid_generated_data(self, send_notification):
        sender = NotificationSender()
        email = self.emails[0]
        sender.send_notification(email, self.data, self.message)

        self.assertEqual(send_notification.call_count, 1)
        send_notification.assert_called_once()

        body = {
            'filters': [
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': email},
            ],
            'data': self.data,
            'contents': {'en': self.message},
        }
        send_notification.assert_called_with(body)

    @mock.patch(
        'onesignal_sdk.client.Client.send_notification',
        return_value=None
    )
    def test_one_email_list_param_call_provider_with_valid_generated_data(self, send_notification):
        sender = NotificationSender()
        email = self.emails[0]
        sender.send_notification([email], self.data, self.message)

        self.assertEqual(send_notification.call_count, 1)
        send_notification.assert_called_once()

        body = {
            'filters': [
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': email},
            ],
            'data': self.data,
            'contents': {'en': self.message},
        }
        send_notification.assert_called_with(body)

    @mock.patch(
        'onesignal_sdk.client.Client.send_notification',
        return_value=None
    )
    def test_many_email_param_call_provider_with_valid_generated_data(self, send_notification):
        sender = NotificationSender()
        sender.send_notification(self.emails, self.data, self.message)

        self.assertEqual(send_notification.call_count, 1)
        send_notification.assert_called_once()

        body = {
            'filters': [
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': self.emails[0]},
                {'operator': 'OR'},
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': self.emails[1]},
                {'operator': 'OR'},
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': self.emails[2]},
                {'operator': 'OR'},
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': self.emails[3]},
                {'operator': 'OR'},
                {'field': 'tag', 'key': 'email', 'relation': '=', 'value': self.emails[4]},
            ],
            'data': self.data,
            'contents': {'en': self.message},
        }
        send_notification.assert_called_with(body)
