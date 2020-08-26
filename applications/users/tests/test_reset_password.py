from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import UserFactory


fake = Faker()


class RequestResetPasswordTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('rest_password_reset')

    def call_reset_password(self):
        return self.client.post(self.url, self.params)

    def setUp(self):
        self.user = UserFactory(confirmed=True)
        self.params = {'email': self.user.email}

    def test_all_params_right_respond_success(self):
        response = self.call_reset_password()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'Password reset e-mail has been sent.'})

    def test_all_params_right_send_confirmation_email(self):
        self.call_reset_password()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.params['email'], mail.outbox[0].to)

    def test_missing_email_respond_failure(self):
        self.params['email'] = ''

        response = self.call_reset_password()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_email_respond_success(self):
        self.params['email'] = 'fake@email.com'
        response = self.call_reset_password()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'Password reset e-mail has been sent.'})


class ConfirmResetPasswordTests(APITestCase):
    def build_params(self):
        return {
            'uid': self.uid,
            'token': self.token,
            'new_password1': self.new_password,
            'new_password2': self.new_password,
        }

    def call_confirm_password(self, params):
        url = reverse('password_reset_confirm', args=(self.uid, self.token, ))
        return self.client.post(url, params)

    def setUp(self):
        self.user = UserFactory(confirmed=True)
        self.new_password = fake.password(length=8)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_all_params_right_respond_success(self):
        params = self.build_params()
        response = self.call_confirm_password(params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'detail': 'Password has been reset with the new password.'}
        )

    def test_log_in_with_new_credentials_successfully(self):
        params = self.build_params()
        response = self.call_confirm_password(params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.post(
            reverse('rest_login'),
            {
                'email': self.user.email,
                'password': self.new_password
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_respond_failure(self):
        self.token = 'fake-token'
        params = self.build_params()

        response = self.call_confirm_password(params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'token': ['Invalid value']})

    def test_invalid_uid_respond_failure(self):
        self.uid = 'fake'
        params = self.build_params()

        response = self.call_confirm_password(params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'uid': ['Invalid value']})
