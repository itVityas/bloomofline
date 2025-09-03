from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from apps.account.models import User, Role, UserRoles


class UserCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='ASDqwe12#'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='SDFwer23$'
        )
        self.admin = User.objects.create_superuser(
            username='testadmin',
            password='ASDqwe12#'
        )
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', args=[self.user.id])
        self.create_url = reverse('register')
        self.change_password_url = reverse('change_user_password')
        self.update_user = reverse('user-update', args=[self.user.id])

    def test_user_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'username': 'XXXXXXX',
            'password': 'ASDqwe12#',
            'password2': 'ASDqwe12#',
            'fio': 'New User',
            'departmant': 'IT',
            'position': 'Developer',
            'room': '101'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_password(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'id': self.user2.id,
            'password': 'ASDqwe12#',
            'password2': 'ASDqwe12#'
        }
        response = self.client.patch(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'username': 'testuser',
            'fio': 'New User',
            'departmant': 'IT',
            'position': 'Developer',
            'room': '101'
        }
        response = self.client.put(self.update_user, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(self.update_user, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_role_delete(self):
        self.client.force_authenticate(user=self.admin)
        role = Role.objects.create(name='testrole', description='testrole')
        UserRoles.objects.create(user=self.user, role=role)
        userroledelete = reverse('userroledelete')
        userroledelete += f'?user={self.user.id}&role={role.id}'
        response = self.client.delete(userroledelete)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
