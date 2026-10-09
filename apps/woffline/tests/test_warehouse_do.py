import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from bloomofline.global_state import global_state
from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles
from apps.aonec.models import OfflineOneCTTN, OfflineOneCTTNItem
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

        cls.model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        cls.model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')

        cls.model1 = OfflineModels.objects.create(id=1, code=111000, name=cls.model_name1, production_code=111)
        cls.model2 = OfflineModels.objects.create(id=2, code=111001, name=cls.model_name2, production_code=222)

        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn1, model_name=cls.model_name1, count=3)
        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn1, model_name=cls.model_name2, count=12)
        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn2, model_name=cls.model_name2, count=10)

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

    def warehousedo_barcode_payload(self):
        data = {
                    'warehouse_id': self.warehouse2.name,
                    'barcode': self.product1.barcode,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                    'warehouse_ttn_number': self.warehouse_ttn2.ttn_number,
                    'warehouse_action_id': self.action1.name,
                }
        return data

    def warehousedo_shipment_payload(self):
        data = {
                    'warehouse_id': self.warehouse2.name,
                    'barcode': self.product1.barcode,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                    'warehouse_ttn_number': self.warehouse_ttn3.ttn_number,
                    'warehouse_action_id': self.action3.name,
                    'model_name_id': self.model_name2.id,
                    'onec_ttn': self.ttn1.number
                }
        return data

    def warehousedo_pallet_payload(self):
        data = {
                    'warehouse_id': self.warehouse2.name,
                    'barcode': self.product3.barcode,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                    'warehouse_ttn_number': self.warehouse_ttn2.ttn_number,
                    'warehouse_action_id': self.action2.name,
                    'model_name_id': self.model_name2.id
                }
        return data

    def warehousedo_shipment_delete_payload(self):
        data = {
            'barcode': self.product1.barcode,
            'new_ttn': self.warehouse_ttn1.ttn_number,
            'onec_number': self.ttn1.number,
            'warehouse_id': self.warehouse1.name,
            'warehouse_action_id': self.action1.name,
            'onec_series': self.ttn1.series,
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
            }
        return data

    def test_warehousedo_update_noauth(self):
        response = self.client.get(reverse('warehousedo-update', kwargs={'pk': self.warehouse_ttn1.ttn_number}),
                                   {'product': self.product2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_update_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('warehousedo-update', kwargs={'pk': self.warehouse_ttn1.ttn_number}),
                                   {'product': self.product2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehousedo_update_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehousedo-update', kwargs={'pk': self.warehouse_ttn1.ttn_number}),
                                   {'product': self.product2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehousedo_barcode_noauth(self):
        response = self.client.post(reverse('warehousedo-barcode'),
                                    self.warehousedo_barcode_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_barcode_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('warehousedo-barcode'),
                                    self.warehousedo_barcode_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehousedo_barcode_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('warehousedo-barcode'),
                                    self.warehousedo_barcode_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offline_warehousedo_barcode_noauth(self):
        response = self.client.post(reverse('offline-warehousedo-barcode'),
                                    self.warehousedo_barcode_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehousedo_barcode_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('offline-warehousedo-barcode'),
                                    self.warehousedo_barcode_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offline_warehousedo_barcode_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('offline-warehousedo-barcode'),
                                    self.warehousedo_barcode_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_warehousedo_pallet_noauth(self):
        response = self.client.post(reverse('warehousedo-pallet'),
                                    self.warehousedo_pallet_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_pallet_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('warehousedo-pallet'),
                                    self.warehousedo_pallet_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehousedo_pallet_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('warehousedo-pallet'),
                                    self.warehousedo_pallet_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offline_warehousedo_pallet_noauth(self):
        response = self.client.post(reverse('offline-warehousedo-pallet'),
                                    self.warehousedo_pallet_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehousedo_pallet_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('offline-warehousedo-pallet'),
                                    self.warehousedo_pallet_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offline_warehousedo_pallet_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('offline-warehousedo-pallet'),
                                    self.warehousedo_pallet_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offline_warehousedo_retrieve_update_destroy_noauth(self):
        response = self.client.delete(reverse('offline-warehousedo-retrieve-update-destroy',
                                              kwargs={'pk': self.warehousedo1.warehouse_ttn}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehousedo_retrieve_update_destroy_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('offline-warehousedo-retrieve-update-destroy',
                                              kwargs={'pk': self.warehousedo1.warehouse_ttn}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offline_warehousedo_retrieve_update_destroy_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.delete(reverse('offline-warehousedo-retrieve-update-destroy',
                                              kwargs={'pk': self.warehousedo1.warehouse_ttn}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_warehousedo_retrieve_noauth(self):
        response = self.client.get(reverse('warehousedo-retrieve', kwargs={'pk': self.warehouse_ttn1.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_retrieve_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('warehousedo-retrieve', kwargs={'pk': self.warehouse_ttn1.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehousedo_retrieve_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('warehousedo-retrieve', kwargs={'pk': self.warehouse_ttn1.ttn_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offline_warehousedo_shipment_noauth(self):
        response = self.client.post(reverse('offline-warehouse-shipment'),
                                    self.warehousedo_shipment_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehousedo_shipment_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('offline-warehouse-shipment'),
                                    self.warehousedo_shipment_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offline_warehousedo_shipment_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('offline-warehouse-shipment'),
                                    self.warehousedo_shipment_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_warehousedo_shipment_noauth(self):
        response = self.client.post(reverse('warehouse-shipment'),
                                    self.warehousedo_shipment_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_shipment_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('warehouse-shipment'),
                                    self.warehousedo_shipment_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehousedo_shipment_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('warehouse-shipment'),
                                    self.warehousedo_shipment_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_warehousedo_shipment_delete_noauth(self):
        response = self.client.post(reverse('warehousedo-shipment-delete'),
                                    self.warehousedo_shipment_delete_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_warehousedo_shipment_delete_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('warehousedo-shipment-delete'),
                                    self.warehousedo_shipment_delete_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_warehousedo_shipment_delete_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('warehousedo-shipment-delete'),
                                    self.warehousedo_shipment_delete_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offline_warehousedo_shipment_delete_noauth(self):
        response = self.client.post(reverse('offline-warehousedo-shipment-delete'),
                                    self.warehousedo_shipment_delete_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offline_warehousedo_shipment_delete_no_rights(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('offline-warehousedo-shipment-delete'),
                                    self.warehousedo_shipment_delete_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offline_warehousedo_shipment_delete_rights(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('offline-warehousedo-shipment-delete'),
                                    self.warehousedo_shipment_delete_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
