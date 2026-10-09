import datetime

from rest_framework.test import APITestCase

from apps.osgp.models import OfflineShipmentBans, OfflineStorageLimits
from apps.ashtrih.models import OfflineModelNames, OfflineModels


class OSGPTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
        cls.model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')
        cls.model_name3 = OfflineModelNames.objects.create(id=3, name='Test Object XXXX-0002', short_name='XXXX-0002')

        cls.model1 = OfflineModels.objects.create(id=1, code=11333, name=cls.model_name1, production_code=111)
        cls.model2 = OfflineModels.objects.create(id=2, code=11334, name=cls.model_name2, production_code=222)

        cls.limit1 = OfflineStorageLimits.objects.create(max_storage_days=15, production_code='0001', model_code='0000')
        OfflineShipmentBans.objects.create(order_number='000111', order_date=datetime.datetime.now(),
                                           model_name_id=cls.model_name1, barcode='0000111122', apply_to_belarus=True)

    def test_get_shipment_ban(self):
        response = OfflineShipmentBans.objects.get(order_number='000111')
        self.assertEqual('000111', response.order_number)

    def test_create_shipment_ban(self):
        response = OfflineShipmentBans.objects.create(order_number='000112', order_date=datetime.datetime.now(),
                                                      model_name_id=self.model_name2, barcode='0000111123',
                                                      apply_to_belarus=True)
        self.assertEqual(response.order_number, '000112')
        self.assertEqual(response.barcode, '0000111123')

    def test_delete_shipment_ban(self):
        ban = OfflineShipmentBans.objects.create(order_number='000112', order_date=datetime.datetime.now(),
                                                 model_name_id=self.model_name2, barcode='0000111123',
                                                 apply_to_belarus=True)
        ban.delete()
        is_exists = OfflineShipmentBans.objects.filter(order_number='000112').exists()
        self.assertFalse(is_exists)

    def test_update_shipment_ban(self):
        ban = OfflineShipmentBans.objects.get(order_number='000111')
        ban.apply_to_belarus = False
        ban.save()
        updated_ban = OfflineShipmentBans.objects.get(order_number='000111')
        self.assertFalse(updated_ban.apply_to_belarus)

    def test_get_storage_limit(self):
        response = OfflineStorageLimits.objects.get(id=self.limit1.id)
        self.assertEqual(1, response.id)

    def test_create_storage_limit(self):
        response = OfflineStorageLimits.objects.create(max_storage_days=20, production_code='0002', model_code='0002')
        self.assertEqual(response.id, 2)
        self.assertEqual(response.max_storage_days, 20)

    def test_delete_storage_limit(self):
        limit = OfflineStorageLimits.objects.create(max_storage_days=20, production_code='0002', model_code='0002')
        limit.delete()
        is_exists = OfflineStorageLimits.objects.filter(id=limit.id).exists()
        self.assertFalse(is_exists)

    def test_update_storage_limit(self):
        limit = OfflineStorageLimits.objects.get(id=self.limit1.id)
        limit.max_storage_days = 30
        limit.production_code = 2002
        limit.save()
        updated_limit = OfflineStorageLimits.objects.get(id=self.limit1.id)
        self.assertEqual(updated_limit.max_storage_days, 30)
        self.assertEqual(updated_limit.production_code, 2002)
