import datetime

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from urllib.parse import urlencode

from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles


class UserTest(APITestCase):
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

    def test_details_user_noauth(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_details_user_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_noauth(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('user-update', kwargs={'pk': 2}), {'fio': 'New FIO'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(reverse('user-update', kwargs={'pk': 2}), {'fio': 'New FIO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_role_no_rights(self):
        self.client.force_authenticate(user=self.user)
        needed_role = OfflineRole.objects.get(name='ban')
        response = self.client.delete(reverse('userroledelete')
                                      + '?'
                                      + urlencode({'user': self.admin.id, 'role': needed_role.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_role(self):
        self.client.force_authenticate(user=self.admin)
        needed_role = OfflineRole.objects.get(name='ban')
        response = self.client.delete(reverse('userroledelete')
                                      + '?'
                                      + urlencode({'user': self.admin.id, 'role': needed_role.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
