from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from apps.account.models import User, Role


class TestUserRoles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='XXXXXXXX',
            password='XXXXXXXXXXXX'
        )
        self.role = Role.objects.create(
            name='test1',
            description='test1'
        )
        self.client.force_authenticate(user=self.user)
        self.user_role_list_create_url = reverse('userrole-list')
        self.user_role_detailed_url = reverse('userrole-detailed', args=[1])

    def test_user_role_create(self):
        data = {
            'user': self.user.id,
            'role': self.role.id
        }
        response = self.client.post(self.user_role_list_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_role_list(self):
        response = self.client.get(self.user_role_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_role_update(self):
        data = {
            'user': self.user.id,
            'role': self.role.id
        }
        response = self.client.put(self.user_role_detailed_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
