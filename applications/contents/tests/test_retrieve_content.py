from faker import Faker
from faker.providers import lorem
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import ContentFactory
from applications.contents.models import Content
from applications.users.tests.factories import UserFactory


fake = Faker()
fake.add_provider(lorem)


class ContentRetrieveTest(APITestCase):
    def call_get_content_by_key(self, key):
        url = reverse('content-detail', args=(key,))
        return self.client.get(url)

    def test_no_created_content_return_not_found(self):
        key = fake.word()

        response = self.call_get_content_by_key(key)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.user = UserFactory(confirmed=True)
        self.client.force_authenticate(user=self.user)
        response = self.call_get_content_by_key(key)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_created_content_and_wrong_key_return_not_found(self):
        ContentFactory()
        self.assertTrue(Content.objects.exists())

        key = fake.word()

        response = self.call_get_content_by_key(key)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.user = UserFactory(confirmed=True)
        self.client.force_authenticate(user=self.user)
        response = self.call_get_content_by_key(key)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_created_content_return_founded(self):
        content = ContentFactory()
        self.assertTrue(Content.objects.exists())

        response = self.call_get_content_by_key(content.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user = UserFactory(confirmed=True)
        self.client.force_authenticate(user=self.user)
        response = self.call_get_content_by_key(content.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_created_topics_return_topics(self):
        content = ContentFactory()
        self.assertTrue(Content.objects.exists())

        response = self.call_get_content_by_key(content.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(
            [key for key in response_json],
            ['key', 'title', 'body', ]
        )
        self.assertEqual(response_json['key'], content.key)
        self.assertEqual(response_json['title'], content.title)
        self.assertEqual(response_json['body'], content.body)
