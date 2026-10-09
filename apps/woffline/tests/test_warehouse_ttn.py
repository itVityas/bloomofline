import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from urllib.parse import urlencode

from bloomofline.global_state import global_state
from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles
from apps.aonec.models import OfflineOneCTTN
from apps.ashtrih.models import OfflineModelNames, OfflineModels, OfflineProducts
from apps.woffline.models import OfflineWarehouse, OfflineTypeOfWork, OfflineWarehouseAction, OfflineWarehouseTTN
from apps.woffline.models import OfflinePallet, OfflineWarehouseDo, OfflineOldProduct

from apps.woffline.utils.generate_barcode import generate_barcode


class TTNTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = OfflineUser.objects.create_user(id=1, username='test_user',
                                                   password='testpassword', updated_at=datetime.datetime.now())
        cls.warehouse = OfflineUser.objects.create_user(id=2, username='test_warehouse',
                                                        password='testpassword', updated_at=datetime.datetime.now())

        warehouse_role = OfflineRole.objects.create(id=1, name='warehouse_writer', update_at=datetime.datetime.now())

        OfflineUserRoles.objects.create(id=1, user=cls.warehouse,
                                        role=warehouse_role, update_at=datetime.datetime.now())

        cls.ttn1 = OfflineOneCTTN.objects.create(number='0001', series='XXX')
        cls.ttn2 = OfflineOneCTTN.objects.create(number='0002', series='YYY')
        cls.ttn3 = OfflineOneCTTN.objects.create(number='0003', series='ZZZ')

        cls.model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        cls.model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')
        cls.model_name3 = OfflineModelNames.objects.create(id=3, name='Test Object XXXX-0002', short_name='XXXX-0002')

        cls.model1 = OfflineModels.objects.create(id=1, code=111000, name=cls.model_name1, production_code=111)
        cls.model2 = OfflineModels.objects.create(id=2, code=111001, name=cls.model_name2, production_code=222)

        cls.warehouse1 = OfflineWarehouse.objects.create(name='1')
        cls.warehouse2 = OfflineWarehouse.objects.create(name='2')

        cls.work_type1 = OfflineTypeOfWork.objects.create(name='Операции склада')
        cls.work_type2 = OfflineTypeOfWork.objects.create(name='Паллетирование')
        cls.work_type3 = OfflineTypeOfWork.objects.create(name='Отгрузка')

        cls.action1 = OfflineWarehouseAction.objects.create(name='1', type_of_work=cls.work_type1)
        cls.action2 = OfflineWarehouseAction.objects.create(name='2', type_of_work=cls.work_type2)
        cls.action3 = OfflineWarehouseAction.objects.create(name='3', type_of_work=cls.work_type3)

        cls.warehouse_ttn1 = OfflineWarehouseTTN.objects.create(ttn_number='001', warehouse=cls.warehouse1,
                                                                warehouse_action=cls.action1, onec_ttn=cls.ttn1,
                                                                user=cls.warehouse, date=datetime.datetime.now())
        cls.warehouse_ttn2 = OfflineWarehouseTTN.objects.create(ttn_number='002', warehouse=cls.warehouse1,
                                                                warehouse_action=cls.action2, onec_ttn=cls.ttn2,
                                                                user=cls.warehouse, date=datetime.datetime.now())
        cls.warehouse_ttn3 = OfflineWarehouseTTN.objects.create(ttn_number='003', warehouse=cls.warehouse1,
                                                                warehouse_action=cls.action3, onec_ttn=cls.ttn2,
                                                                user=cls.warehouse, date=datetime.datetime.now())

        cls.product1 = OfflineProducts.objects.create(id=1, barcode="0001", model=cls.model1, state=0,
                                                      available_quantity=3, type_of_work_id=3,
                                                      work_date=datetime.datetime.now(), module_id=1)
        cls.product2 = OfflineProducts.objects.create(id=2, barcode="0002", model=cls.model2, state=0,
                                                      available_quantity=5, type_of_work_id=3,
                                                      work_date=datetime.datetime.now(), module_id=2)
        cls.product3 = OfflineProducts.objects.create(id=3, barcode="0003", model=cls.model2, state=0,
                                                      available_quantity=5, type_of_work_id=cls.work_type3.id,
                                                      work_date=datetime.datetime.now(), module_id=2)

        cls.old_product1 = OfflineOldProduct.objects.create(barcode=generate_barcode(cls.warehouse_ttn1.ttn_number),
                                                            model=cls.model1, state=1, quantity=1)
        cls.old_product2 = OfflineOldProduct.objects.create(barcode=generate_barcode(cls.warehouse_ttn2.ttn_number),
                                                            model=cls.model2, state=1, quantity=1)

        cls.warehousedo1 = OfflineWarehouseDo.objects.create(warehouse_ttn=cls.warehouse_ttn1, product=cls.product1,
                                                             old_product=cls.old_product1)
        cls.warehousedo2 = OfflineWarehouseDo.objects.create(warehouse_ttn=cls.warehouse_ttn2, product=cls.product2,
                                                             old_product=cls.old_product2)

        cls.pallet1 = OfflinePallet.objects.create(ttn_number=cls.warehouse_ttn1,
                                                   barcode=generate_barcode(cls.warehouse_ttn1))

    def setUp(self):
        global_state.set_false()

    def warehouse_ttn_payload(self):
        ttn4 = OfflineOneCTTN.objects.create(number='0004')
        data = {
                    'ttn_number': '010',
                    'warehouse': self.warehouse1.name,
                    'warehouse_action': self.action1.name,
                    'onec_ttn': ttn4.number
                }
        return data

    def test_warehousedo_list_noauth(self):
        response = self.client.get(reverse('warehousedo-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehousedo-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_ttn_list_noauth(self):
        response = self.client.get(reverse('warehouse-ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offline_warehouse_ttn_list_noauth(self):
        response = self.client.get(reverse('offline-warehouse-ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehouse_ttn_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('offline-warehouse-ttn-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_ttn_create_noauth(self):
        response = self.client.post(reverse('warehouse-ttn-create'),
                                    self.warehouse_ttn_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_create_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('warehouse-ttn-create'),
                                    self.warehouse_ttn_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('error', response.data)

    def test_warehouse_ttn_create_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('warehouse-ttn-create'),
                                    self.warehouse_ttn_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('error', response.data)

    def test_warehouse_ttn_update_noauth(self):
        response = self.client.patch(reverse('warehouse-ttn-update', kwargs={'ttn_number': '001'}),
                                     {'warehouse_action': self.action1.name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_warehouse_ttn_update_norights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('warehouse-ttn-update', kwargs={'ttn_number': '001'}),
                                     {'warehouse_action': self.action1.name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('error', response.data)

    def test_warehouse_ttn_update_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.patch(reverse('warehouse-ttn-update', kwargs={'ttn_number': '001'}),
                                     {'warehouse_action': self.action1.name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)

    def test_warehouse_ttn_retrieve_noauth(self):
        response = self.client.get(reverse('warehouse-ttn-retrieve',
                                           kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_retrieve_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('warehouse-ttn-retrieve',
                                           kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehouse_ttn_retrieve_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-ttn-retrieve',
                                           kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_ttn_user_noauth(self):
        response = self.client.get(reverse('warehouse-ttn-user'), {'user_id': self.warehouse.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_user_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-ttn-user'), {'user_id': self.warehouse.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_ttn_products_list_noauth(self):
        response = self.client.get(reverse('warehouse-ttn-products-list',
                                           kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_products_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-ttn-products-list',
                                           kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_ttn_by_user_products_list_noauth(self):
        response = self.client.get(reverse('warehouse-ttn-products-by-user-list')
                                   + '?'
                                   + urlencode({'user_id': self.warehouse.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_by_user_products_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-ttn-products-by-user-list')
                                   + '?'
                                   + urlencode({'user_id': self.warehouse.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offline_warehouse_ttn_by_user_products_list_noauth(self):
        response = self.client.get(reverse('offline-warehouse-ttn-products-by-user-list')
                                   + '?'
                                   + urlencode({'user_id': self.warehouse.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehouse_ttn_by_user_products_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('offline-warehouse-ttn-products-by-user-list')
                                   + '?'
                                   + urlencode({'user_id': self.warehouse.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_ttn_by_onec_products_list_noauth(self):
        response = self.client.get(reverse('warehouse-ttn-products-by-onec-list')
                                   + '?'
                                   + urlencode({'series': self.ttn1.series, 'number': self.ttn1.number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehouse_ttn_by_onec_products_listt_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehouse-ttn-products-by-onec-list')
                                   + '?'
                                   + urlencode({'series': self.ttn1.series, 'number': self.ttn1.number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offline_warehouse_ttn_by_onec_products_list_noauth(self):
        response = self.client.get(reverse('offline-warehouse-ttn-products-by-onec-list')
                                   + '?'
                                   + urlencode({'series': self.ttn1.series, 'number': self.ttn1.number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehouse_ttn_by_onec_products_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('offline-warehouse-ttn-products-by-onec-list')
                                   + '?'
                                   + urlencode({'series': self.ttn1.series, 'number': self.ttn1.number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offline_warehouse_ttn_update_noauth(self):
        response = self.client.delete(reverse('offline-warehouse-ttn-update',
                                              kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehouse_ttn_update_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('offline-warehouse-ttn-update',
                                              kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offline_warehouse_ttn_update(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.delete(reverse('offline-warehouse-ttn-update',
                                              kwargs={'ttn_number': self.warehouse_ttn2.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
