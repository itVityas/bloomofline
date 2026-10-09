import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from bloomofline.global_state import global_state
from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles
from apps.aonec.models import OfflineOneCTTN
from apps.woffline.models import OfflineWarehouse, OfflineTypeOfWork, OfflineWarehouseAction


class WarehouseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.warehouse = OfflineUser.objects.create_user(id=2, username='test_warehouse',
                                                        password='testpassword', updated_at=datetime.datetime.now())

        warehouse_role = OfflineRole.objects.create(id=1, name='warehouse_writer', update_at=datetime.datetime.now())

        OfflineUserRoles.objects.create(id=1, user=cls.warehouse,
                                        role=warehouse_role, update_at=datetime.datetime.now())

        cls.ttn1 = OfflineOneCTTN.objects.create(number='0001', series='XXX')
        cls.ttn2 = OfflineOneCTTN.objects.create(number='0002', series='YYY')
        cls.ttn3 = OfflineOneCTTN.objects.create(number='0003', series='ZZZ')

        cls.warehouse1 = OfflineWarehouse.objects.create(name='1')
        cls.warehouse2 = OfflineWarehouse.objects.create(name='2')

        cls.work_type1 = OfflineTypeOfWork.objects.create(name='Операции склада')
        cls.work_type2 = OfflineTypeOfWork.objects.create(name='Паллетирование')

        cls.action1 = OfflineWarehouseAction.objects.create(name='1', type_of_work=cls.work_type1)
        cls.action2 = OfflineWarehouseAction.objects.create(name='2', type_of_work=cls.work_type2)

    def setUp(self):
        global_state.set_false()

    def test_warehouse_type_of_work_list_noauth(self):
        response = self.client.get(reverse('type-of-work-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_type_of_work_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('type-of-work-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_action_list_noauth(self):
        response = self.client.get(reverse('action-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_action_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('action-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_detailed_action_list_noauth(self):
        response = self.client.get(reverse('detailed-action-list', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_detailed_action_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('detailed-action-list', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_list_noauth(self):
        response = self.client.get(reverse('warehouse-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
