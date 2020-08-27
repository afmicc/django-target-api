from django.db import transaction

from channels.db import database_sync_to_async
import environ
from onesignal_sdk.client import Client as OneSignalClient, AsyncClient as OneSignalAsyncClient

from .models import Notification

env = environ.Env()


class NotificationSender:
    client_params = {
        'app_id': env('ONESIGNAL_APP_ID'),
        'rest_api_key': env('ONESIGNAL_API_KEY')
    }

    def send_notification(self, emails, data, message):
        body = self._body(emails, data, message)

        client = OneSignalClient(**self.client_params)
        client.send_notification(body)

    async def send_notification_async(self, emails, data, message):
        body = self._body(emails, data, message)

        client = OneSignalAsyncClient(**self.client_params)
        await client.send_notification(body)

    def _body(self, emails, data, message):
        return {
            'filters': self._create_filter_by_emails(emails),
            'data': data,
            'contents': {'en': message},
        }

    def _create_filter_by_emails(self, emails):
        email_list = emails if type(emails) is list else [emails]

        return [self._filter_option(email_list, i) for i in range(len(email_list*2) - 1)]

    def _filter_option(self, options, index):
        return self._email_filter(options[int(index/2)]) if index % 2 == 0 else {'operator': 'OR'}

    def _email_filter(self, email):
        return {'field': 'tag', 'key': 'email', 'relation': '=', 'value': email}


class NotificationCreator:
    sender = NotificationSender()

    @transaction.atomic
    def create(self, user, data, title, message):
        Notification.objects.create(user=user, title=title, message=message)

        self.sender.send_notification(user.email, data, message)

    async def create_async(self, user, data, title, message):
        await database_sync_to_async(
            Notification.objects.create
        )(user=user, title=title, message=message)

        await self.sender.send_notification_async(user.email, data, message)
