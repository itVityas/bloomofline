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
from apps.woffline.models import OfflinePallet, OfflineWarehouseDo

from apps.woffline.utils.generate_barcode import generate_barcode


class PalletTest(APITestCase):
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

        cls.model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        cls.model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')

        cls.model1 = OfflineModels.objects.create(id=1, code=11333, name=cls.model_name1, production_code=111)
        cls.model2 = OfflineModels.objects.create(id=2, code=11334, name=cls.model_name2, production_code=222)

        cls.warehouse1 = OfflineWarehouse.objects.create(name='1')
        cls.warehouse2 = OfflineWarehouse.objects.create(name='2')

        cls.work_type1 = OfflineTypeOfWork.objects.create(name='Операции склада')
        cls.work_type2 = OfflineTypeOfWork.objects.create(name='Паллетирование')

        cls.action1 = OfflineWarehouseAction.objects.create(name='1', type_of_work=cls.work_type1)
        cls.action2 = OfflineWarehouseAction.objects.create(name='2', type_of_work=cls.work_type2)

        cls.warehouse_ttn1 = OfflineWarehouseTTN.objects.create(ttn_number='536030', warehouse=cls.warehouse1,
                                                                warehouse_action=cls.action1, onec_ttn=cls.ttn1,
                                                                user=cls.warehouse, date=datetime.datetime.now())
        cls.warehouse_ttn2 = OfflineWarehouseTTN.objects.create(ttn_number='536031', warehouse=cls.warehouse2,
                                                                warehouse_action=cls.action2, onec_ttn=cls.ttn2,
                                                                user=cls.warehouse, date=datetime.datetime.now())

        cls.product1 = OfflineProducts.objects.create(id=1, barcode='000000000000000001', model=cls.model1, state=0,
                                                      available_quantity=3, type_of_work_id=3,
                                                      work_date=datetime.datetime.now(), module_id=1)
        cls.product2 = OfflineProducts.objects.create(id=2, barcode='000000000000000002', model=cls.model2, state=0,
                                                      available_quantity=5, type_of_work_id=2,
                                                      work_date=datetime.datetime.now(), module_id=2)

        cls.warehousedo1 = OfflineWarehouseDo.objects.create(warehouse_ttn=cls.warehouse_ttn1, product=cls.product1,
                                                             )
        cls.warehousedo2 = OfflineWarehouseDo.objects.create(warehouse_ttn=cls.warehouse_ttn2, product=cls.product2,
                                                             )

        cls.pallet1 = OfflinePallet.objects.create(ttn_number=cls.warehouse_ttn1,
                                                   barcode=generate_barcode(cls.warehouse_ttn1))
        cls.pallet2 = OfflinePallet.objects.create(ttn_number=cls.warehouse_ttn2,
                                                   barcode=generate_barcode(cls.warehouse_ttn2))

    def setUp(self):
        global_state.set_false()

    def test_pallet_list_noauth(self):
        response = self.client.get(reverse('pallet-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_pallet_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('pallet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)

    def test_pallet_update_noauth(self):
        response = self.client.delete(reverse('pallet-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_pallet_update_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('pallet-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('error', response.data)

    def test_pallet_update_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.delete(reverse('pallet-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)

    def test_pallet_create_noauth(self):
        response = self.client.post(reverse('pallet-create'), {
            'ttn_number': self.warehouse_ttn1.ttn_number,
            'barcode': generate_barcode(ttn_number=self.warehouse_ttn1.ttn_number)
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_pallet_create_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('pallet-create'), {
            'ttn_number': self.warehouse_ttn1.ttn_number,
            'barcode': generate_barcode(ttn_number=self.warehouse_ttn1.ttn_number)
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('error', response.data)

    def test_pallet_create_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('pallet-create'), {
            'ttn_number': self.warehouse_ttn1.ttn_number,
            'barcode': generate_barcode(ttn_number=self.warehouse_ttn1.ttn_number)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('error', response.data)

    def test_pallet_with_products_list_noauth(self):
        response = self.client.get(reverse('pallet-with-products-list')
                                   + '?'
                                   + urlencode({'ttn_number': self.warehouse_ttn1.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_pallet_with_products_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('pallet-with-products-list')
                                   + '?'
                                   + urlencode({'ttn_number': self.warehouse_ttn1.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)

    def test_offline_pallet_with_products_by_barcode_list_noauth(self):
        response = self.client.get(reverse('offline-pallet-by-barcode-list')
                                   + '?'
                                   + urlencode({'barcode': self.pallet1.barcode}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_offline_pallet_with_products_by_barcode_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('offline-pallet-by-barcode-list')
                                   + '?'
                                   + urlencode({'barcode': self.pallet1.barcode}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)

    def test_pallet_with_products_by_barcode_list_noauth(self):
        response = self.client.get(reverse('pallet-by-barcode-list')
                                   + '?'
                                   + urlencode({'barcode': self.pallet1.barcode}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_pallet_with_products_by_barcode_list_auth(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('pallet-by-barcode-list')
                                   + '?'
                                   + urlencode({'barcode': self.pallet1.barcode}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)

    def test_decompose_noauth(self):
        response = self.client.get(reverse('decompose')
                                   + '?'
                                   + urlencode({'barcode': self.pallet2.barcode}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_decompose_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('decompose')
                                   + '?'
                                   + urlencode({'barcode': self.pallet2.barcode}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('error', response.data)

    def test_decompose_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('decompose')
                                   + '?'
                                   + urlencode({'barcode': self.pallet2.barcode}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)
