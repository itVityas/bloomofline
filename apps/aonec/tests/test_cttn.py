import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from bloomofline.global_state import global_state
from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles
from apps.aonec.models import OfflineOneCTTN, OfflineOneCTTNItem
from apps.ashtrih.models import OfflineModelNames


class TTNTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = OfflineUser.objects.create_user(id=1, username='test_admin',
                                                    password='testpassword', updated_at=datetime.datetime.now())
        cls.user = OfflineUser.objects.create_user(id=2, username='test_user',
                                                   password='testpassword', updated_at=datetime.datetime.now())
        cls.warehouse = OfflineUser.objects.create_user(id=3, username='test_warehouse',
                                                        password='testpassword', updated_at=datetime.datetime.now())

        admin_role = OfflineRole.objects.create(id=1, name='admin', update_at=datetime.datetime.now())
        warehouse_role = OfflineRole.objects.create(id=3, name='warehouse_writer', update_at=datetime.datetime.now())

        OfflineUserRoles.objects.create(id=1, user=cls.admin,
                                        role=admin_role, update_at=datetime.datetime.now())
        OfflineUserRoles.objects.create(id=2, user=cls.warehouse,
                                        role=warehouse_role, update_at=datetime.datetime.now())

        ttn1 = OfflineOneCTTN.objects.create(number='0001')
        ttn2 = OfflineOneCTTN.objects.create(number='0002')

        model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')

        OfflineOneCTTNItem.objects.create(onec_ttn=ttn1, model_name=model_name1, count=3)
        OfflineOneCTTNItem.objects.create(onec_ttn=ttn1, model_name=model_name2, count=12)
        OfflineOneCTTNItem.objects.create(onec_ttn=ttn2, model_name=model_name2, count=10)

    def setUp(self):
        global_state.set_false()

    def test_ttn_details_noauth(self):
        response = self.client.get(reverse('ttn-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ttn_details_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ttn-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ttn_details_has_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('ttn-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ttn_list_noauth(self):
        response = self.client.get(reverse('ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ttn_list_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ttn_list_has_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)
