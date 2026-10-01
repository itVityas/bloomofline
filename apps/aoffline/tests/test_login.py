import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.aoffline.models import OfflineUser


class LoginTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = OfflineUser.objects.create_user(id=1, username='test_admin',
                                                    password='testpassword', updated_at=datetime.datetime.now())

    def test_login_success(self):
        data = {
            'username': 'test_admin',
            'password': 'testpassword'
        }

        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_failure(self):
        data = {
            'username': 'test_admin',
            'password': 'wrong_password'
        }

        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
