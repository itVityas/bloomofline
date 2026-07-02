import time
from datetime import timedelta

from django.db import transaction
import logging

from apps.sgp.models import ShipmentBans
from apps.osgp.models import OfflineShipmentBans
from apps.sync.models import SyncDate

logger = logging.getLogger(__name__)


class SGPFullSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.sync_date = sync_date
        self.batch_size = batch_size
        self.sync_date.last_sync = self.sync_date.last_sync - timedelta(hours=3)

    def full_sync(self) -> dict:
        try:
            with transaction.atomic():
                time_full = dict()
                time_ban = self.bans_full_sync()
                time_full['ban'] = time_ban
                time_full['full'] = time_ban
                return time_full
        except Exception as e:
            logger.error('onec full sync: ' + str(e))
            raise e

    def bans_full_sync(self) -> float:
        try:
            start_time = time.time()
            OfflineShipmentBans.objects.all().delete()
            bans_items = ShipmentBans.objects.all().order_by('id').values(
                'id', 'order_number', 'order_date', 'order_number', 'order_date',
                'start_date', 'end_date', 'production_code_id_id', 'model_name_id_id', 'barcode',
                'color_id__color_code', 'module_id_id', 'shift',
                'pakaging_date_from', 'pakaging_date_to', 'is_active', 'apply_to_belarus',
                'created_at', 'updated_at')
            list_bans = []
            for i in bans_items.iterator(chunk_size=self.batch_size):
                list_bans.append(OfflineShipmentBans(
                    id=i['id'],
                    order_number=i['order_number'],
                    order_date=i['order_date'],
                    start_date=i['start_date'],
                    end_date=i['end_date'],
                    production_code=i['production_code_id_id'],
                    model_name_id_id=i['model_name_id_id'],
                    barcode=i['barcode'],
                    color_code=i['color_id__color_code'],
                    module_id=i['module_id_id'],
                    shift=i['shift'],
                    pakaging_date_from=i['pakaging_date_from'],
                    pakaging_date_to=i['pakaging_date_to'],
                    is_active=i['is_active'],
                    apply_to_belarus=i['apply_to_belarus'],
                    created_at=i['created_at'],
                    updated_at=i['updated_at']
                ))
                if len(list_bans) >= self.batch_size:
                    OfflineShipmentBans.objects.bulk_create(list_bans)
                    list_bans.clear()
            if list_bans:
                OfflineShipmentBans.objects.bulk_create(list_bans)
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('bans_full_sync:' + str(e))
            raise e


class SGPSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.sync_date = sync_date
        self.batch_size = batch_size
        self.sync_date.last_sync = self.sync_date.last_sync - timedelta(hours=3)

    def sync(self) -> dict:
        try:
            time_full = dict()
            time_ban = self.ban_sync()
            time_full['ban'] = time_ban
            time_full['full'] = time_ban
            return time_full
        except Exception as e:
            logger.error('onec sync: ' + str(e))
            raise e

    def ban_sync(self) -> float:
        try:
            start_time = time.time()
            bans = ShipmentBans.objects.filter(updated_at__gt=self.sync_date.last_sync).values(
                'id', 'order_number', 'order_date', 'order_number', 'order_date',
                'start_date', 'end_date', 'production_code_id_id', 'model_name_id_id', 'barcode',
                'color_id__color_code', 'module_id_id', 'shift',
                'pakaging_date_from', 'pakaging_date_to', 'is_active', 'apply_to_belarus',
                'created_at', 'updated_at')
            existing_ids = set(OfflineShipmentBans.objects.values_list('id', flat=True))
            list_ban = []
            list_update = []
            buf = 0
            for i in bans.iterator(chunk_size=self.batch_size):
                buf += 1
                if i['id'] in existing_ids:
                    list_update.append(i)
                else:
                    list_ban.append(OfflineShipmentBans(
                        id=i['id'],
                        order_number=i['order_number'],
                        order_date=i['order_date'],
                        start_date=i['start_date'],
                        end_date=i['end_date'],
                        production_code=i['production_code_id_id'],
                        model_name_id_id=i['model_name_id_id'],
                        barcode=i['barcode'],
                        color_code=i['color_id__color_code'],
                        module_id=i['module_id_id'],
                        shift=i['shift'],
                        pakaging_date_from=i['pakaging_date_from'],
                        pakaging_date_to=i['pakaging_date_to'],
                        is_active=i['is_active'],
                        apply_to_belarus=i['apply_to_belarus'],
                        created_at=i['created_at'],
                        updated_at=i['updated_at']
                    ))
                if buf >= self.batch_size:
                    OfflineShipmentBans.objects.bulk_create(list_ban)
                    list_ban.clear()
                    buf = 0
            if list_ban:
                OfflineShipmentBans.objects.bulk_create(list_ban)
            if list_update:
                for i in list_update:
                    OfflineShipmentBans.objects.filter(id=i['id']).update(
                        order_number=i['order_number'],
                        order_date=i['order_date'],
                        message=i['message'],
                        start_date=i['start_date'],
                        end_date=i['end_date'],
                        production_code=i['production_code_id_id'],
                        model_name_id_id=i['model_name_id_id'],
                        barcode=i['barcode'],
                        color_code=i['color_id__color_code'],
                        module_id=i['module_id_id'],
                        shift=i['shift'],
                        assembly_date_from=i['assembly_date_from'],
                        assembly_date_to=i['assembly_date_to'],
                        pakaging_date_from=i['pakaging_date_from'],
                        pakaging_date_to=i['pakaging_date_to'],
                        is_active=i['is_active'],
                        apply_to_belarus=i['apply_to_belarus'],
                        created_at=i['created_at'],
                        updated_at=i['updated_at']
                    )
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('onec_ttn_sync: ' + str(e))
            raise e
