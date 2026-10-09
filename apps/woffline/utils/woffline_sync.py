import time
from datetime import datetime

from django.db import transaction, connection
from django.db.models.functions import Now
import logging

from apps.sync.models import SyncDate
from apps.woffline.models import (
    OfflineTypeOfWork,
    OfflineWarehouseAction,
    OfflineWarehouse,
    OfflineWarehouseDo,
    OfflineWarehouseTTN,
    OfflinePallet,
    OfflineOldProduct,
    OfflineNotPackaging,
)
from apps.warehouse.models import (
    TypeOfWork,
    WarehouseAction,
    Pallet,
    Warehouse,
    WarehouseTTN,
    OldProduct,
    WarehouseDo,
    NotPackaging,
)
from bloomofline.json_writer import json_writer

logger = logging.getLogger(__name__)


def pallet_upload(update_date: datetime = None):
    pallets = OfflinePallet.objects.filter(is_offline=True)
    data_json = []
    for i in pallets.iterator(chunk_size=1000):
        data_json.append({
            'ttn_number': i.ttn_number_id,
            'barcode': i.barcode,
            'is_deleted': i.is_deleted,
        })
        Pallet.objects.update_or_create(
            ttn_number_id=i.ttn_number_id,
            barcode=i.barcode,
            defaults={
                'is_deleted': i.is_deleted,
                'update_at': Now(),
            }
        )
    json_writer(data_json, 'pallet')
    pallets.delete()


def warehouse_ttn_upload(update_date: datetime = None):
    warehouse_ttn = OfflineWarehouseTTN.objects.filter(is_offline=True)
    data_json = []
    for i in warehouse_ttn:
        data_json.append({
            'ttn_number': i.ttn_number,
            'user_id': i.user_id,
            'warehouse_id': i.warehouse_id,
            'warehouse_action_id': i.warehouse_action_id,
            'is_close': i.is_close,
            'date': i.date,
            'onec_ttn_id': i.onec_ttn_id,
            'is_deleted': i.is_deleted,
        })
        WarehouseTTN.objects.update_or_create(
            ttn_number=i.ttn_number,
            user_id=i.user_id,
            warehouse_id=i.warehouse_id,
            warehouse_action_id=i.warehouse_action_id,
            defaults={
                'is_close': i.is_close,
                'date': i.date,
                'onec_ttn_id': i.onec_ttn_id,
                'is_deleted': i.is_deleted,
                'update_at': Now(),
            }
        )
    json_writer(data_json, 'warehouse_ttn')
    warehouse_ttn.update(is_offline=False)


def warehouse_do_upload(update_date: datetime = None):
    warehouse_do = OfflineWarehouseDo.objects.filter(is_offline=True)
    data_json = []
    for i in warehouse_do.iterator(chunk_size=1000):
        data_json.append(
            {
                'warehouse_ttn_id': i.warehouse_ttn_id,
                'product': i.product_id,
                'old_product': i.old_product_id,
                'quantity': i.quantity,
                'is_deleted': i.is_deleted,
            }
        )
        WarehouseDo.objects.update_or_create(
            id=i.id,
            warehouse_ttn_id=i.warehouse_ttn_id,
            product_id=i.product_id,
            old_product_id=i.old_product_id,
            defaults={
                'quantity': i.quantity,
                'is_deleted': i.is_deleted,
                'update_at': Now(),
            }
        )
    json_writer(data_json, 'warehouse_do')
    warehouse_do.delete()


def not_packaging_upload():
    not_packaging = OfflineNotPackaging.objects.filter(is_offline=True)
    not_packaging_list = []
    for i in not_packaging:
        not_packaging_list.append(
            NotPackaging(
                product_id=i.product_id,
                warehouse_id=i.warehouse_id,
                bloom_user_id=i.bloom_user_id,
                found_date=i.found_date,
                solve_date=i.solve_date,
                is_solved=i.is_solved,
            )
        )
    not_packaging.delete()
    NotPackaging.objects.bulk_create(not_packaging_list)


class WarehouseFullSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 2000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def _executemany(self, sql: str, qs) -> int:
        batch, total = [], 0
        with connection.cursor() as cursor:
            for row in qs.iterator(chunk_size=self.batch_size):
                batch.append(row)
                if len(batch) >= self.batch_size:
                    cursor.executemany(sql, batch)
                    total += len(batch)
                    batch.clear()
            if batch:
                cursor.executemany(sql, batch)
                total += len(batch)
        return total

    def full_sync(self):
        try:
            time_full = dict()
            time_full['type_of_work'] = self.type_of_work_full_sync()
            time_full['action'] = self.action_full_sync()
            time_full['warehouse'] = self.warehouse_full_sync()
            time_full['ttn'] = self.warehouse_ttn_full_sync()
            time_full['pallet'] = self.pallet_full_sync()
            time_full['old_product'] = self.old_product_full_sync()
            time_full['do'] = self.warehouse_do_full_sync()
            time_full['not_packaging'] = self.NotPackaging_full_sync()
            time_full['full'] = sum(time_full.values())
            return time_full
        except Exception as e:
            logger.error('full_sync: ' + str(e))
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
                'id',
                'name',
                'type_of_work_id',
                'operation',
                'is_deleted',
                'create_at',
                'update_at'
            )
            bulk_list = []
            for i in action_list:
                bulk_list.append(OfflineWarehouseAction(
                    id=i['id'],
                    name=i['name'],
                    type_of_work_id=i['type_of_work_id'],
                    operation=i['operation'],
                    is_deleted=i['is_deleted'],
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
            pallet_list = Pallet.objects.all().values_list(
                'id', 'ttn_number', 'barcode', 'is_deleted', 'create_at', 'update_at',
                named=False
            )
            PALLET_INSERT_SQL = """
                INSERT INTO woffline_offlinepallet
                    (id, ttn_number_id, barcode, is_deleted, create_at, update_at, is_offline)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """
            self._executemany(PALLET_INSERT_SQL, pallet_list)
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
            warehouse_ttn_list = WarehouseTTN.objects.all().values_list(
                'ttn_number', 'is_close', 'date', 'warehouse_id', 'warehouse_action_id',
                'onec_ttn_id', 'user_id', 'is_deleted', 'create_at', 'update_at',
                named=False
            )
            TTN_INSERT_SQL = """
                INSERT INTO woffline_offlinewarehousettn
                    (ttn_number, is_close, date, warehouse_id, warehouse_action_id,
                    onec_ttn_id, user_id, is_deleted, create_at, update_at, is_offline)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """
            self._executemany(TTN_INSERT_SQL, warehouse_ttn_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_ttn_full_sync' + str(e))
            raise e

    def old_product_full_sync(self):
        try:
            start_time = time.time()
            old_product_list = OldProduct.objects.all().values(
                'id', 'barcode', 'color_id', 'model_id', 'state', 'quantity', 'is_shipment',
            )
            bulk_list = []
            for i in old_product_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineOldProduct(
                    id=i['id'],
                    barcode=i['barcode'],
                    color_id=i['color_id'],
                    model_id=i['model_id'],
                    state=i['state'],
                    quantity=i['quantity'],
                    is_shipment=i['is_shipment'],
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
            warehouse_do_list = WarehouseDo.objects.all().values_list(
                'id', 'warehouse_ttn_id', 'product_id', 'quantity', 'old_product_id',
                'create_at', 'update_at', 'is_deleted',
                named=False
            )
            SQL_WAREHOUSEDO_INSERT = """
                INSERT INTO woffline_offlinewarehousedo
                (id, warehouse_ttn_id, product_id, quantity, old_product_id,
                create_at, update_at, is_deleted, is_offline)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            """
            self._executemany(SQL_WAREHOUSEDO_INSERT, warehouse_do_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_do_full_sync' + str(e))
            raise e

    def NotPackaging_full_sync(self):
        try:
            start_time = time.time()
            not_packaging_list = NotPackaging.objects.all().values(
                'id', 'product_id', 'warehouse_id', 'bloom_user_id', 'found_date',
                'solve_date', 'is_solved',
            )
            bulk_list = []
            for i in not_packaging_list.iterator(chunk_size=self.batch_size):
                bulk_list.append(OfflineNotPackaging(
                    id=i['id'],
                    product_id=i['product_id'],
                    warehouse_id=i['warehouse_id'],
                    bloom_user_id=i['bloom_user_id'],
                    found_date=i['found_date'],
                    solve_date=i['solve_date'],
                    is_solved=i['is_solved'],
                    is_offline=False,
                ))
                if len(bulk_list) >= self.batch_size:
                    OfflineNotPackaging.objects.bulk_create(bulk_list)
                    bulk_list.clear()
            if bulk_list:
                OfflineNotPackaging.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('NotPackaging_full_sync' + str(e))
            raise e


class WarehouseSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 10000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def sync(self):
        try:
            time_sync = {}
            with transaction.atomic():
                time_sync['type_of_work'] = self.type_of_work_sync()
                time_sync['action'] = self.action_sync()
                time_sync['warehouse'] = self.warehouse_sync()
                time_sync['ttn'] = self.warehouse_ttn_sync()
                time_sync['pallet'] = self.pallet_sync()
                time_sync['old_product'] = self.old_product_sync()
                time_sync['do'] = self.warehouse_do_sync()
                time_sync['not_packaging'] = self.not_packaging_sync()
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
                'id',
                'name',
                'type_of_work_id',
                'operation',
                'is_deleted',
                'create_at',
                'update_at'
            )
            bulk_list = []
            for i in action_list:
                bulk_list.append(OfflineWarehouseAction(
                    id=i['id'],
                    name=i['name'],
                    type_of_work_id=i['type_of_work_id'],
                    operation=i['operation'],
                    is_deleted=i['is_deleted'],
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
                'id', 'barcode', 'color_id', 'model_id', 'state', 'quantity', 'is_shipment',
            )
            bulk_list = []
            for i in old_product_list:
                bulk_list.append(OfflineOldProduct(
                    id=i['id'],
                    barcode=i['barcode'],
                    color_id=i['color_id'],
                    model_id=i['model_id'],
                    state=i['state'],
                    quantity=i['quantity'],
                    is_shipment=i['is_shipment'],
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
            pallet_upload(self.sync_date.last_sync)
            pallet_list = Pallet.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'barcode', 'ttn_number', 'is_deleted', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in pallet_list:
                ttn = OfflineWarehouseTTN.objects.get(ttn_number=i['ttn_number'])
                bulk_list.append(OfflinePallet(
                    id=i['id'],
                    ttn_number=ttn,
                    barcode=i['barcode'],
                    is_deleted=i['is_deleted'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            # вначале все удаляем, потом создаем заново, первый вариант, дольше по времени
            # OfflinePallet.objects.filter(
            #     id__in=[i.id for i in bulk_list]
            # ).delete()
            # OfflinePallet.objects.bulk_create(bulk_list)
            OfflinePallet.objects.bulk_create(
                bulk_list,
                update_conflicts=True,
                unique_fields=['id'],
                update_fields=['barcode', 'ttn_number', 'create_at', 'update_at', 'is_offline', 'is_deleted'])
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('pallet_sync ' + str(e))
            raise e

    def warehouse_ttn_sync(self):
        try:
            start_time = time.time()
            warehouse_ttn_upload(self.sync_date.last_sync)
            warehouse_ttn_list = WarehouseTTN.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'ttn_number', 'is_close', 'date', 'warehouse_id', 'warehouse_action_id',
                'onec_ttn_id', 'user_id', 'is_deleted', 'create_at', 'update_at'
            )
            bulk_list = []
            for i in warehouse_ttn_list:
                bulk_list.append(OfflineWarehouseTTN(
                    ttn_number=i['ttn_number'],
                    is_close=i['is_close'],
                    date=i['date'],
                    warehouse_id=i['warehouse_id'],
                    warehouse_action_id=i['warehouse_action_id'],
                    onec_ttn_id=i['onec_ttn_id'],
                    user_id=i['user_id'],
                    is_deleted=i['is_deleted'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_offline=False,
                ))
            # вначале все удаляем, потом создаем заново, первый вариант, дольше по времени
            # OfflineWarehouseTTN.objects.filter(
            #     ttn_number__in=[i.ttn_number for i in bulk_list]
            # ).delete()
            # OfflineWarehouseTTN.objects.bulk_create(bulk_list)
            OfflineWarehouseTTN.objects.bulk_create(
                bulk_list,
                update_conflicts=True,
                unique_fields=['ttn_number'],
                update_fields=['is_close', 'date', 'warehouse_id', 'warehouse_action_id',
                               'onec_ttn_id', 'user_id', 'is_deleted', 'create_at', 'update_at', 'is_offline'])
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_ttn_sync ' + str(e))
            raise e

    def warehouse_do_sync(self):
        try:
            start_time = time.time()
            warehouse_do_upload(self.sync_date.last_sync)
            warehouse_do_list = WarehouseDo.objects.filter(
                update_at__gt=self.sync_date.last_sync
            ).values(
                'id', 'warehouse_ttn_id', 'product_id', 'quantity', 'old_product_id',
                'create_at', 'update_at', 'is_deleted',
            )
            bulk_list = []
            for i in warehouse_do_list:
                bulk_list.append(OfflineWarehouseDo(
                    id=i['id'],
                    warehouse_ttn_id=i['warehouse_ttn_id'],
                    product_id=i['product_id'],
                    quantity=i['quantity'],
                    old_product_id=i['old_product_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                    is_deleted=i['is_deleted'],
                    is_offline=False,
                ))
            # вначале все удаляем, потом создаем заново, первый вариант, дольше по времени
            # OfflineWarehouseDo.objects.filter(
            #     id__in=[i.id for i in bulk_list]
            # ).delete()
            # OfflineWarehouseDo.objects.bulk_create(bulk_list)
            OfflineWarehouseDo.objects.bulk_create(
                bulk_list,
                update_conflicts=True,
                unique_fields=['id'],
                update_fields=['warehouse_ttn_id', 'product_id', 'quantity', 'old_product_id',
                               'create_at', 'update_at', 'is_offline', 'is_deleted']
            )
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('warehouse_do_sync' + str(e))
            raise e

    def not_packaging_sync(self):
        try:
            start_time = time.time()
            not_packaging_upload()
            not_packaging_list = NotPackaging.objects.filter(
                solve_date__gt=self.sync_date.last_sync
            ).values(
                'id', 'product_id', 'warehouse_id', 'bloom_user_id', 'found_date',
                'solve_date', 'is_solved',
            )
            bulk_list = []
            for i in not_packaging_list:
                bulk_list.append(OfflineNotPackaging(
                    id=i['id'],
                    product_id=i['product_id'],
                    warehouse_id=i['warehouse_id'],
                    bloom_user_id=i['bloom_user_id'],
                    found_date=i['found_date'],
                    solve_date=i['solve_date'],
                    is_solved=i['is_solved'],
                ))
            OfflineNotPackaging.objects.bulk_create(bulk_list)
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error('not_packaging_sync' + str(e))
            raise e
