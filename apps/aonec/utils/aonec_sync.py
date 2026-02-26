import time

from django.db import transaction
import logging

from apps.onec.models import OneCTTN, OneCTTNItem
from apps.aonec.models import (
    OfflineOneCTTN as offline_OneCTTN,
    OfflineOneCTTNItem as offline_OneCTTItem
)
from apps.sync.models import SyncDate

logger = logging.getLogger(__name__)


class OneCFullSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def full_sync(self) -> dict:
        try:
            with transaction.atomic():
                time_full = dict()
                time_ttn = self.onec_ttn_full_sync()
                time_item = self.onec_ttn_item_full_sync()
                time_full['ttn'] = time_ttn
                time_full['ttn_item'] = time_item
                time_full['full'] = time_ttn + time_item
                return time_full
        except Exception as e:
            raise e

    def onec_ttn_full_sync(self) -> float:
        try:
            start_time = time.time()
            offline_OneCTTN.objects.all().delete()
            onec_ttn = OneCTTN.objects.all().order_by('id').values(
                'id', 'number', 'series', 'create_at', 'update_at')
            list_ttn = []
            for i in onec_ttn.iterator(chunk_size=self.batch_size):
                list_ttn.append(offline_OneCTTN(
                    id=i['id'],
                    number=i['number'],
                    series=i['series'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                ))
                if len(list_ttn) >= self.batch_size:
                    offline_OneCTTN.objects.bulk_create(list_ttn)
                    list_ttn.clear()
            if list_ttn:
                offline_OneCTTN.objects.bulk_create(list_ttn)
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('onec_ttn_full_sync' + str(e))
            raise e

    def onec_ttn_item_full_sync(self) -> float:
        try:
            start_time = time.time()
            offline_OneCTTItem.objects.all().delete()
            onec_ttn_items = OneCTTNItem.objects.select_related('onec_ttn').all().order_by('id').values(
                'id', 'onec_ttn_id', 'name', 'count', 'create_at', 'update_at')
            list_ttn_item = []
            for i in onec_ttn_items.iterator(chunk_size=self.batch_size):
                list_ttn_item.append(offline_OneCTTItem(
                    id=i['id'],
                    onec_ttn_id=i['onec_ttn_id'],
                    name=i['name'],
                    count=i['count'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                ))
                if len(list_ttn_item) >= self.batch_size:
                    offline_OneCTTItem.objects.bulk_create(list_ttn_item)
                    list_ttn_item.clear()
            if list_ttn_item:
                offline_OneCTTItem.objects.bulk_create(list_ttn_item)
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('onec_ttn_item_full_sync' + str(e))
            raise e


class OneCSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def sync(self) -> dict:
        try:
            with transaction.atomic():
                time_full = dict()
                time_ttn = self.onec_ttn_sync()
                time_item = self.onec_ttn_item_sync()
                time_full['ttn'] = time_ttn
                time_full['ttn_item'] = time_item
                time_full['full'] = time_ttn + time_item
                return time_full
        except Exception as e:
            raise e

    def onec_ttn_sync(self) -> float:
        try:
            start_time = time.time()
            last_onec_ttn = offline_OneCTTN.objects.order_by('-id').first()
            onec_tnn = OneCTTN.objects.filter(id__gt=last_onec_ttn.id if last_onec_ttn else 0).values(
                'id', 'number', 'series', 'create_at', 'update_at')
            existing_ids = set(offline_OneCTTN.objects.values_list('id', flat=True))
            list_ttn = []
            list_update = []
            buf = 0
            for i in onec_tnn.iterator(chunk_size=self.batch_size):
                buf += 1
                if i['id'] in existing_ids:
                    list_update.append(i)
                else:
                    list_ttn.append(offline_OneCTTN(
                        id=i['id'],
                        number=i['number'],
                        series=i['series'],
                        create_at=i['create_at'],
                        update_at=i['update_at'],
                    ))
                if buf >= self.batch_size:
                    offline_OneCTTN.objects.bulk_create(list_ttn)
                    list_ttn.clear()
                    buf = 0
            if list_ttn:
                offline_OneCTTN.objects.bulk_create(list_ttn)
            if list_update:
                for i in list_update:
                    offline_OneCTTN.objects.filter(id=i['id']).update(
                        number=i['number'],
                        series=i['series'],
                        create_at=i['created_at'],
                        update_at=i['updated_at'],
                    )
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('onec_ttn_sync' + str(e))
            raise e

    def onec_ttn_item_sync(self) -> float:
        try:
            start_time = time.time()
            last_onec_ttn_item = offline_OneCTTItem.objects.order_by('-id').first()
            onec_ttn_item = OneCTTNItem.objects.filter(
                id__gt=last_onec_ttn_item.id if last_onec_ttn_item else 0).values(
                'id', 'onec_ttn_id', 'name', 'count', 'create_at', 'update_at')
            existing_ids = set(offline_OneCTTItem.objects.values_list('id', flat=True))
            list_items = []
            list_update = []
            buf = 0
            for i in onec_ttn_item.iterator(chunk_size=self.batch_size):
                buf += 1
                if i['id'] in existing_ids:
                    list_update.append(i)
                else:
                    list_items.append(offline_OneCTTItem(
                        id=i['id'],
                        onec_ttn_id=i['onec_ttn_id'],
                        name=i['name'],
                        count=i['count'],
                        create_at=i['create_at'],
                        update_at=i['update_at'],
                    ))
                if buf >= self.batch_size:
                    offline_OneCTTItem.objects.bulk_create(list_items)
                    list_items.clear()
                    buf = 0
            if list_items:
                offline_OneCTTItem.objects.bulk_create(list_items)
            if list_update:
                for i in list_update:
                    offline_OneCTTItem.objects.filter(id=i['id']).update(
                        onec_ttn_id=i['onec_ttn_id'],
                        name=i['name'],
                        count=i['count'],
                        create_at=i['create_at'],
                        update_at=i['update_at'],
                    )
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('onec_ttn_item_sync' + str(e))
            raise e
