from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from apps.account.models import User, Role


class RoleCRUDTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='testadmin',
            password='ASDqwe12#'
        )
        self.role = Role.objects.create(name="Test Role")
        self.client.force_authenticate(user=self.admin)
        self.list_create_url = reverse('listcreate-role')
        self.update_url = reverse('update-role', kwargs={'pk': self.role.pk})

    def test_list_roles(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_role(self):
        data = {'name': 'New Role'}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_role(self):
        data = {'name': 'Updated Role'}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_role(self):
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
