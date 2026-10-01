# import datetime

# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.urls import reverse

# from bloomofline.global_state import global_state
# from apps.aoffline.models import OfflineUser, OfflineRole, OfflineUserRoles
# from apps.aonec.models import OfflineOneCTTN, OfflineOneCTTNItem
# from apps.ashtrih.models import OfflineModelNames
# from apps.woffline.models import OfflineWarehouse, OfflineTypeOfWork, OfflineWarehouseAction, OfflineWarehouseTTN


# class TTNTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = OfflineUser.objects.create_user(id=1, username='test_user',
#                                                    password='testpassword', updated_at=datetime.datetime.now())
#         cls.warehouse = OfflineUser.objects.create_user(id=2, username='test_warehouse',
#                                                         password='testpassword', updated_at=datetime.datetime.now())

#         warehouse_role = OfflineRole.objects.create(id=1, name='warehouse_writer', update_at=datetime.datetime.now())

#         OfflineUserRoles.objects.create(id=1, user=cls.warehouse,
#                                         role=warehouse_role, update_at=datetime.datetime.now())

#         ttn1 = OfflineOneCTTN.objects.create(number='0001')
#         ttn2 = OfflineOneCTTN.objects.create(number='0002')
#         ttn3 = OfflineOneCTTN.objects.create(number='0003')

#         model_name1 = OfflineModelNames.objects.create(id=1, name='Test Object XXXX-0000', short_name='XXXX-0000')
#         model_name2 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0001', short_name='XXXX-0001')
#         model_name3 = OfflineModelNames.objects.create(id=2, name='Test Object XXXX-0002', short_name='XXXX-0002')

#         OfflineOneCTTNItem.objects.create(onec_ttn=ttn1, model_name=model_name1, count=3)
#         OfflineOneCTTNItem.objects.create(onec_ttn=ttn1, model_name=model_name2, count=12)
#         OfflineOneCTTNItem.objects.create(onec_ttn=ttn2, model_name=model_name2, count=10)
#         OfflineOneCTTNItem.objects.create(onec_ttn=ttn3, model_name=model_name3, count=5)

#         OfflineWarehouse.objects.create(name='W1')
#         OfflineWarehouse.objects.create(name='W2')

#         work_type1 = OfflineTypeOfWork.objects.create(name='T1')
#         work_type2 = OfflineTypeOfWork.objects.create(name='T2')

#         action1 = OfflineWarehouseAction(name='', type_of_work=work_type1)
#         action2 = OfflineWarehouseAction(name='', type_of_work=work_type2)

#         warehouse_ttn1 = OfflineWarehouseTTN.objects.create(ttn_name='001', warehouse=warehouse1, warehouse_action=action1,
#                                                             onec_ttn=ttn1, user=cls.warehouse)
#         warehouse_ttn2 = OfflineWarehouseTTN.objects.create(ttn_name='002', warehouse=warehouse1, warehouse_action=action2,
#                                                             onec_ttn=ttn2, user=cls.warehouse)
#         warehouse_ttn3 = OfflineWarehouseTTN.objects.create(ttn_name='003', warehouse=warehouse1, warehouse_action=action2,
#                                                             onec_ttn=ttn3, user=cls.warehouse)

#     def setUp(self):
#         global_state.set_false()

#     def test_warehouse_ttn_list(self):
#         pass
