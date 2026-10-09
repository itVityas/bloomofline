import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles


class RoleTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = OfflineUser.objects.create_user(id=1, username='test_admin',
                                                    password='testpassword', updated_at=datetime.datetime.now())

        cls.user = OfflineUser.objects.create_user(id=2, username='test_user',
                                                   password='testpassword', updated_at=datetime.datetime.now())

        admin_role = OfflineRole.objects.create(id=1, name='admin', update_at=datetime.datetime.now())
        user_role = OfflineRole.objects.create(id=2, name='ban', update_at=datetime.datetime.now())

        OfflineUserRoles.objects.create(id=1, user=cls.admin, role=admin_role, update_at=datetime.datetime.now())
        OfflineUserRoles.objects.create(id=2, user=cls.user, role=user_role, update_at=datetime.datetime.now())

    def test_role_list_noauth(self):
        response = self.client.get(reverse('userrole-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_role_list_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('userrole-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_details_role_noauth(self):
        response = self.client.get(reverse('userrole-detailed', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_details_role_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('userrole-detailed', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_role_no_rights(self):
        self.client.force_authenticate(user=self.user)
        data = {'id': 3, 'name': 'Test role', 'update_at': datetime.datetime.now()}
        response = self.client.post(reverse('listcreate-role'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'id': 3, 'name': 'Test role', 'update_at': datetime.datetime.now()}
        response = self.client.post(reverse('listcreate-role'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_role_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('update-role', kwargs={'pk': 1}), {'name': 'New name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(reverse('update-role', kwargs={'pk': 1}), {'name': 'New name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
