import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from bloomofline.global_state import global_state
from apps.aoffline.models import OfflineRole, OfflineUser, OfflineUserRoles
from apps.ashtrih.models import OfflineModelNames, OfflineModels, OfflineProducts


class ProductTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = OfflineUser.objects.create_user(id=1, username='test_admin',
                                                    password='testpassword', updated_at=datetime.datetime.now())

        admin_role = OfflineRole.objects.create(id=1, name='admin', update_at=datetime.datetime.now())

        OfflineUserRoles.objects.create(id=1, user=cls.admin, role=admin_role,
                                        create_at=datetime.datetime.now(), update_at=datetime.datetime.now())

        model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')

        model1 = OfflineModels.objects.create(id=1, code=111000, name=model_name1, production_code=111)
        model2 = OfflineModels.objects.create(id=2, code=111001, name=model_name2, production_code=222)

        OfflineProducts.objects.create(id=1, barcode="0001", model=model1, state=0, available_quantity=3,
                                       type_of_work_id=1, work_date=datetime.datetime.now(), module_id=1)
        OfflineProducts.objects.create(id=2, barcode="0002", model=model2, state=0, available_quantity=5,
                                       type_of_work_id=1, work_date=datetime.datetime.now(), module_id=1)

    def setUp(cls):
        global_state.set_false()

    def test_product_list_noauth(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('error', response.data)

    def test_product_list_auth(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)
