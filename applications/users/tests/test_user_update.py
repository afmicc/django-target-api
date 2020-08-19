import factory
import io
from faker import Faker
from PIL import Image
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import BaseUserFactory, UserFactory
from applications.users.models import User


class UserFieldsUpdateTests(APITestCase):
    fake = Faker()

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('rest_user_details')

    def setUp(self):
        self.email = self.fake.email()
        self.user = UserFactory(email=self.email, confirmed=True)
        self.params = factory.build(dict, FACTORY_CLASS=BaseUserFactory, email=self.email)

    def call_update(self):
        self.client.force_authenticate(user=self.user)
        return self.client.put(self.url, self.params)

    def get_user(self):
        return User.objects.get(email=self.user.email)

    def test_all_params_valid_respond_success(self):
        response = self.call_update()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [key for key in response.json()],
            ['id', 'email', 'name', 'gender', 'picture', ]
        )

    def test_all_params_valid_save_data(self):
        response = self.call_update()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = self.get_user()
        self.assertEqual(self.params['email'], user.email)
        self.assertEqual(self.params['name'], user.name)
        self.assertEqual(self.params['gender'], user.gender)

    def test_all_params_valid_change_data(self):
        prev_email = self.user.email
        prev_name = self.user.name
        prev_gender = self.user.gender

        response = self.call_update()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.params['email'], prev_email)
        self.assertNotEqual(self.params['name'], prev_name)
        self.assertNotEqual(self.params['gender'], prev_gender)

    def test_missing_name_respond_success_and_not_change_data(self):
        prev_name = self.user.name
        del self.params['name']

        response = self.call_update()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_user().name, prev_name)

    def test_missing_gender_respond_success_and_not_change_data(self):
        prev_gender = self.user.gender
        del self.params['gender']

        response = self.call_update()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_user().gender, prev_gender)

    def test_no_loged_user_respond_unauthorized(self):
        self.user = None
        response = self.call_update()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_user_picture_respond_success_and_store(self):
        self.assertIsNone(self.user.picture.name)

        self.client.force_authenticate(user=self.user)
        data = {'picture': self.generate_photo_file()}
        response = self.client.put(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['picture'])
        self.assertIsNotNone(self.get_user().picture.name)
