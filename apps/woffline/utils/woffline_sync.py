import time

from django.db import transaction
import logging

from apps.sync.models import SyncDate
from apps.woffline.models import (
    OfflineTypeOfWork,
    OfflineWarehouseAction,
    OfflineWarehouse,
    OfflineWarehouseDo,
    OfflineWarehouseTTN,
    OfflinePallet,
    OfflineWarehouseProduct,
    OfflineShipment,
    OfflineOldProduct,
)
from apps.warehouse.models import (
    TypeOfWork,
    WarehouseAction,
    Pallet,
    Warehouse,
    WarehouseTTN,
    WarehouseProduct,
    Shipment,
    OldProduct,
    WarehouseDo,
)


logger = logging.getLogger(__name__)


def pallet_upload():
    pallet = OfflinePallet.objects.filter(is_offline=True).values(
        'barcode', 'create_at', 'update_at')
    pallet_list = []
    for i in pallet:
        pallet_list.append(
            Pallet(
                barcode=i['barcode'],
                create_at=i['create_at'],
                update_at=i['update_at'],
            )
        )
        i.delete()
    Pallet.objects.bulk_create(pallet_list)


def warehouse_ttn_upload():
    warehouse_ttn = OfflineWarehouseTTN.objects.filter(is_offline=True).values(
        'ttn_number', 'is_close', 'date', 'warehouse_id', 'warehouse_action_id',
        'pallet_id', 'user_id', 'create_at', 'update_at'
    )
    warehouse_ttn_list = []
    for i in warehouse_ttn:
        warehouse_ttn_list.append(
            WarehouseTTN(
                ttn_number=i['ttn_number'],
                is_close=i['is_close'],
                date=i['date'],
                warehouse_id=i['warehouse_id'],
                warehouse_action_id=i['warehouse_action_id'],
                pallet=i['pallet'],
                user_id=i['user_id'],
                create_at=i['create_at'],
                update_at=i['update_at'],
            )
        )
        i.delete()
    WarehouseTTN.objects.bulk_create(warehouse_ttn_list)


def warehouse_product_upload():
    warehouse_product = OfflineWarehouseProduct.objects.filter(is_offline=True).values(
        'product_id', 'quantity', 'is_shipment', 'create_at', 'update_at'
    )
    warehouse_product_list = []
    for i in warehouse_product:
        warehouse_product_list.append(
            WarehouseProduct(
                product_id=i['product_id'],
                quantity=i['quantity'],
                is_shipment=i['is_shipment'],
                create_at=i['create_at'],
                update_at=i['update_at'],
            )
        )
        i.delete()
    WarehouseProduct.objects.bulk_create(warehouse_product_list)


def warehouse_do_upload():
    warehouse_do = OfflineWarehouseDo.objects.filter(is_offline=True).values(
        'warehouse_ttn_id', 'warehouse_product_id', 'quantity', 'user_id', 'create_at',
        'update_at'
    )
    warehouse_do_list = []
    for i in warehouse_do:
        warehouse_do_list.append(
            WarehouseDo(
                warehouse_ttn_id=i['warehouse_ttn_id'],
                warehouse_product_id=i['warehouse_product_id'],
                quantity=i['quantity'],
                user_id=i['user_id'],
                create_at=i['create_at'],
                update_at=i['update_at'],
            )
        )
        i.delete()
    WarehouseDo.objects.bulk_create(warehouse_do_list)


def shipment_upload():
    shipments = OfflineShipment.objects.filter(is_offline=True).values(
        'onec_ttn_id', 'warehouse_id', 'warehouse_product_id', 'quantity', 'user_id',
        'create_at', 'update_at'
    )
    shipment_list = []
    for i in shipments:
        shipment_list.append(
            Shipment(
                id=i['id'],
                onec_ttn_id=i['onec_ttn_id'],
                warehouse_id=i['warehouse_id'],
                warehouse_product_id=i['warehouse_product_id'],
                quantity=i['quantity'],
                user_id=i['user_id'],
                create_at=i['create_at'],
                update_at=i['update_at'],
            )
        )
        i.delete()
    Shipment.objects.bulk_create(shipment_list)


class WarehouseFullSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def full_sync(self):
        try:
            time_full = dict()
            with transaction.atomic():
                OfflineOldProduct.objects.all().delete()
                OfflineWarehouseDo.objects.all().delete()
                OfflineShipment.objects.all().delete()
                OfflineWarehouseProduct.objects.all().delete()
                OfflineWarehouseTTN.objects.all().delete()
                OfflineWarehouse.objects.all().delete()
                OfflinePallet.objects.all().delete()
                OfflineWarehouseAction.objects.all().delete()
                OfflineTypeOfWork.objects.all().delete()

                time_full['type_of_work'] = self.type_of_work_full_sync()
                time_full['action'] = self.action_full_sync()
                time_full['pallet'] = self.pallet_full_sync()
                time_full['warehouse'] = self.warehouse_full_sync()
                time_full['ttn'] = self.warehouse_ttn_full_sync()
                time_full['product'] = self.warehouse_product_full_sync()
                time_full['shipment'] = self.shipment_full_sync()
                time_full['old_product'] = self.old_product_sync()
                time_full['do'] = self.warehouse_do_full_sync()
                time_full['full'] = sum(time_full.values())
            return time_full
        except Exception as e:
            logger.error('full_sync' + str(e))
            raise e

    def type_of_work_full_sync(self):
        try:
            start_time = time.time()
            type_of_work_list = TypeOfWork.objects.all().values(
                'id', 'name', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in type_of_work_list:
                bulk_list.append(OfflineTypeOfWork(
                    id=i['id'],
                    name=i['name'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflineTypeOfWork.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('type_of_work_full_sync' + str(e))
            raise e

    def action_full_sync(self):
        try:
            start_time = time.time()
            action_list = WarehouseAction.objects.all().values(
                'id', 'name', 'type_of_work_id', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in action_list:
                bulk_list.append(OfflineWarehouseAction(
                    id=i['id'],
                    name=i['name'],
                    type_of_work_id=i['type_of_work_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflineWarehouseAction.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('action_full_sync' + str(e))
            raise e

    def pallet_full_sync(self):
        try:
            start_time = time.time()
            pallet_upload()
            pallet_list = Pallet.objects.all().values(
                'id', 'barcode', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in pallet_list:
                bulk_list.append(OfflinePallet(
                    id=i['id'],
                    barcode=i['barcode'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflinePallet.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('pallet_full_sync' + str(e))
            raise e

    def warehouse_full_sync(self):
        try:
            start_time = time.time()
            warehouse_list = Warehouse.objects.all().values(
                'id', 'name', 'is_active', 'date', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_list:
                bulk_list.append(OfflineWarehouse(
                    id=i['id'],
                    name=i['name'],
                    is_active=i['is_active'],
                    date=i['date'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflineWarehouse.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_full_sync' + str(e))
            raise e

    def warehouse_ttn_full_sync(self):
        try:
            start_time = time.time()
            warehouse_ttn_upload()
            warehouse_ttn_list = WarehouseTTN.objects.all().values(
                'ttn_number', 'is_close', 'date', 'warehouse_id', 'warehouse_action_id',
                'pallet_id', 'user_id', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_ttn_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineWarehouseTTN(
                    ttn_number=i['ttn_number'],
                    is_close=i['is_close'],
                    date=i['date'],
                    warehouse_id=i['warehouse_id'],
                    warehouse_action_id=i['warehouse_action_id'],
                    pallet_id=i['pallet_id'],
                    user_id=i['user_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
                if len(bulk_list) >= self.batch_size:
                    OfflineWarehouseTTN.objects.bulk_create(bulk_list)
                    bulk_list.clear()
            if bulk_list:
                OfflineWarehouseTTN.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_ttn_full_sync' + str(e))
            raise e

    def warehouse_product_full_sync(self):
        try:
            start_time = time.time()
            warehouse_product_upload()
            warehouse_product_list = WarehouseProduct.objects.all().values(
                'id', 'product_id', 'quantity', 'is_shipment', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_product_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineWarehouseProduct(
                    id=i['id'],
                    product_id=i['product_id'],
                    quantity=i['quantity'],
                    is_shipment=i['is_shipment'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
                if len(bulk_list) >= self.batch_size:
                    OfflineWarehouseProduct.objects.bulk_create(bulk_list)
                    bulk_list.clear()
            if bulk_list:
                OfflineWarehouseProduct.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_product_full_sync' + str(e))
            raise e

    def shipment_full_sync(self):
        try:
            start_time = time.time()
            shipment_upload()
            shipment_list = Shipment.objects.all().values(
                'id', 'onec_ttn_id', 'warehouse_id', 'warehouse_product_id', 'quantity',
                'user_id', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in shipment_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineShipment(
                    id=i['id'],
                    onec_ttn_id=i['onec_ttn_id'],
                    warehouse_id=i['warehouse_id'],
                    warehouse_product_id=i['warehouse_product_id'],
                    quantity=i['quantity'],
                    user_id=i['user_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
                if len(bulk_list) >= self.batch_size:
                    OfflineShipment.objects.bulk_create(bulk_list)
                    bulk_list.clear()
            if bulk_list:
                OfflineShipment.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('shipment_full_sync' + str(e))
            raise e

    def old_product_sync(self):
        try:
            start_time = time.time()
            old_product_list = OldProduct.objects.all().values(
                'id', 'barcode', 'color_id', 'model_id', 'state', 'quantity'
            )
            bulk_list = []
            for i in old_product_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineOldProduct(
                    id=i['id'],
                    barcode=i['barcode'],
                    color_id=i['color_id'],
                    model_id=i['model_id'],
                    state=i['state'],
                    quantity=i['quantity']
                ))
                if len(bulk_list) >= self.batch_size:
                    OfflineOldProduct.objects.bulk_create(bulk_list)
                    bulk_list.clear()
            if bulk_list:
                OfflineOldProduct.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('old_product_sync' + str(e))
            raise e

    def warehouse_do_full_sync(self):
        try:
            start_time = time.time()
            warehouse_do_upload()
            warehouse_do_list = WarehouseDo.objects.all().values(
                'id', 'warehouse_ttn_id', 'warehouse_product_id', 'quantity', 'user_id',
                'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_do_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineWarehouseDo(
                    id=i['id'],
                    warehouse_ttn_id=i['warehouse_ttn_id'],
                    warehouse_product_id=i['warehouse_product_id'],
                    quantity=i['quantity'],
                    user_id=i['user_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
                if len(bulk_list) >= self.batch_size:
                    OfflineWarehouseDo.objects.bulk_create(bulk_list)
                    bulk_list.clear()
            if bulk_list:
                OfflineWarehouseDo.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_do_full_sync' + str(e))
            raise e


class WarehouseSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 10000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def sync(self):
        try:
            time_sync = {}
            time_sync['type_of_work'] = self.type_of_work_sync()
            time_sync['action'] = self.action_sync()
            time_sync['pallet'] = self.pallet_sync()
            time_sync['warehouse'] = self.warehouse_sync()
            time_sync['ttn'] = self.warehouse_ttn_sync()
            time_sync['product'] = self.warehouse_product_sync()
            time_sync['shipment'] = self.shipment_sync()
            time_sync['old_product'] = self.old_product_sync()
            time_sync['do'] = self.warehouse_do_sync()
            time_sync['full'] = sum(time_sync.values())
            return time_sync
        except Exception as e:
            logger.error('sync' + str(e))
            raise e

    def type_of_work_sync(self):
        try:
            start_time = time.time()
            type_of_work_list = TypeOfWork.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'name', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in type_of_work_list:
                bulk_list.append(OfflineTypeOfWork(
                    id=i['id'],
                    name=i['name'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflineTypeOfWork.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflineTypeOfWork.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('type_of_work_sync' + str(e))
            raise e

    def action_sync(self):
        try:
            start_time = time.time()
            action_list = WarehouseAction.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'name', 'type_of_work_id', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in action_list:
                bulk_list.append(OfflineWarehouseAction(
                    id=i['id'],
                    name=i['name'],
                    type_of_work_id=i['type_of_work_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflineWarehouseAction.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflineWarehouseAction.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('action_sync' + str(e))
            raise e

    def warehouse_sync(self):
        try:
            start_time = time.time()
            warehouse_list = Warehouse.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'name', 'is_active', 'date', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_list:
                bulk_list.append(OfflineWarehouse(
                    id=i['id'],
                    name=i['name'],
                    is_active=i['is_active'],
                    date=i['date'],
                    create_at=i['create_at'],
                    update_at=i['update_at']
                ))
            OfflineWarehouse.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflineWarehouse.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_sync' + str(e))
            raise e

    def old_product_sync(self):
        try:
            start_time = time.time()
            last_old_product = OfflineOldProduct.objects.all().order_by('-id').first()
            old_product_list = OldProduct.objects.filter(
                id__gt=last_old_product.id if last_old_product else 0
            ).values(
                'id', 'barcode', 'color_id', 'model_id', 'state', 'quantity'
            )
            bulk_list = []
            for i in old_product_list:
                bulk_list.append(OfflineOldProduct(
                    id=i['id'],
                    barcode=i['barcode'],
                    color_id=i['color_id'],
                    model_id=i['model_id'],
                    state=i['state'],
                    quantity=i['quantity']
                ))
            OfflineOldProduct.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('old_product' + str(e))
            raise e

    def pallet_sync(self):
        try:
            start_time = time.time()
            pallet_upload()
            pallet_list = Pallet.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'barcode', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in pallet_list:
                bulk_list.append(OfflinePallet(
                    id=i['id'],
                    barcode=i['barcode'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            OfflinePallet.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflinePallet.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('pallet_sync' + str(e))
            raise e

    def warehouse_product_sync(self):
        try:
            start_time = time.time()
            warehouse_product_upload()
            warehouse_product_list = WarehouseProduct.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'product_id', 'quantity', 'is_shipment', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_product_list:
                bulk_list.append(OfflineWarehouseProduct(
                    id=i['id'],
                    product_id=i['product_id'],
                    quantity=i['quantity'],
                    is_shipment=i['is_shipment'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            OfflineWarehouseProduct.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflineWarehouseProduct.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_product_sync' + str(e))
            raise e

    def warehouse_ttn_sync(self):
        try:
            start_time = time.time()
            warehouse_ttn_upload()
            warehouse_ttn_list = WarehouseTTN.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'ttn_number', 'is_close', 'date', 'warehouse_id', 'warehouse_action_id',
                'pallet_id', 'user_id', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_ttn_list:
                bulk_list.append(OfflineWarehouseTTN(
                    ttn_number=i['ttn_number'],
                    is_close=i['is_close'],
                    date=i['date'],
                    warehouse_id=i['warehouse_id'],
                    warehouse_action_id=i['warehouse_action_id'],
                    pallet_id=i['pallet_id'],
                    user_id=i['user_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            OfflineWarehouseTTN.objects.filter(
                ttn_number__in=[i.ttn_number for i in bulk_list]
            ).delete()
            OfflineWarehouseTTN.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_ttn_sync' + str(e))
            raise e

    def shipment_sync(self):
        try:
            start_time = time.time()
            shipment_upload()
            shipment_list = Shipment.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'onec_ttn_id', 'warehouse_id', 'warehouse_product_id', 'quantity',
                'user_id', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in shipment_list:
                bulk_list.append(OfflineShipment(
                    id=i['id'],
                    onec_ttn_id=i['onec_ttn_id'],
                    warehouse_id=i['warehouse_id'],
                    warehouse_product_id=i['warehouse_product_id'],
                    quantity=i['quantity'],
                    user_id=i['user_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            OfflineShipment.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflineShipment.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('shipment_sync' + str(e))
            raise e

    def warehouse_do_sync(self):
        try:
            start_time = time.time()
            warehouse_do_upload()
            warehouse_do_list = WarehouseDo.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'warehouse_ttn_id', 'warehouse_product_id', 'quantity', 'user_id',
                'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_do_list:
                bulk_list.append(OfflineWarehouseDo(
                    id=i['id'],
                    warehouse_ttn_id=i['warehouse_ttn_id'],
                    warehouse_product_id=i['warehouse_product_id'],
                    quantity=i['quantity'],
                    user_id=i['user_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            OfflineWarehouseDo.objects.filter(
                id__in=[i.id for i in bulk_list]
            ).delete()
            OfflineWarehouseDo.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_do_sync' + str(e))
            raise e
