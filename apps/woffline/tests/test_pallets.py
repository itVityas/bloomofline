import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from bloomofline.global_state import global_state
from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles
from apps.aonec.models import OfflineOneCTTN, OfflineOneCTTNItem
from apps.ashtrih.models import OfflineModelNames, OfflineModels, OfflineProducts
from apps.woffline.models import OfflineWarehouse, OfflineTypeOfWork, OfflineWarehouseAction, OfflineWarehouseTTN
from apps.woffline.models import OfflinePallet


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

        cls.ttn1 = OfflineOneCTTN.objects.create(number='0001')
        cls.ttn2 = OfflineOneCTTN.objects.create(number='0002')
        cls.ttn3 = OfflineOneCTTN.objects.create(number='0003')

        cls.model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        cls.model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')
        cls.model_name3 = OfflineModelNames.objects.create(id=3, name='Test Object XXXX-0002', short_name='XXXX-0002')

        model1 = OfflineModels.objects.create(id=1, code=111000, name=cls.model_name1, production_code=111)
        model2 = OfflineModels.objects.create(id=2, code=111001, name=cls.model_name2, production_code=222)

        OfflineProducts.objects.create(id=1, barcode="0001", model=model1, state=0, available_quantity=3,
                                       type_of_work_id=1, work_date=datetime.datetime.now(), module_id=1)
        OfflineProducts.objects.create(id=2, barcode="0002", model=model2, state=0, available_quantity=5,
                                       type_of_work_id=1, work_date=datetime.datetime.now(), module_id=1)

        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn1, model_name=cls.model_name1, count=3)
        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn1, model_name=cls.model_name2, count=12)
        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn2, model_name=cls.model_name2, count=10)
        OfflineOneCTTNItem.objects.create(onec_ttn=cls.ttn3, model_name=cls.model_name3, count=5)

        cls.warehouse1 = OfflineWarehouse.objects.create(name='1')
        cls.warehouse2 = OfflineWarehouse.objects.create(name='2')

        cls.work_type1 = OfflineTypeOfWork.objects.create(name='T1')
        cls.work_type2 = OfflineTypeOfWork.objects.create(name='T2')

        cls.action1 = OfflineWarehouseAction.objects.create(name='1', type_of_work=cls.work_type1)
        cls.action2 = OfflineWarehouseAction.objects.create(name='2', type_of_work=cls.work_type2)

        cls.warehouse_ttn1 = OfflineWarehouseTTN.objects.create(ttn_number='001', warehouse=cls.warehouse1,
                                                                warehouse_action=cls.action1, onec_ttn=cls.ttn1,
                                                                user=cls.warehouse)
        cls.warehouse_ttn2 = OfflineWarehouseTTN.objects.create(ttn_number='002', warehouse=cls.warehouse1,
                                                                warehouse_action=cls.action2, onec_ttn=cls.ttn2,
                                                                user=cls.warehouse)

        OfflinePallet.objects.create(ttn_number=cls.warehouse_ttn1, barcode='0001')
        OfflinePallet.objects.create(ttn_number=cls.warehouse_ttn2, barcode='0002')

    def setUp(self):
        global_state.set_false()

    def test_pallet_list(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.get(reverse('pallet-list'))
        print('Warehouse pallets: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pallet_update(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.delete(reverse('pallet-update', kwargs={'pk': 1}))
        print('Warehouse pallets: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pallet_create(self):
        self.client.force_authenticate(user=self.warehouse)
        response = self.client.post(reverse('pallet-create'), {
            'ttn_number': self.warehouse_ttn1.ttn_number,
            'barcode': '0005'
        })
        print('Pallet create: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
