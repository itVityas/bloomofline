import datetime
import time

from apps.onec.models import OneCTTN, OneCTTNItem
from apps.aonec.models import (
    OfflineOneCTTN as offline_OneCTTN,
    OfflineOneCTTNItem as offline_OneCTTItem
)
from apps.ashtrih.models import OfflineModels
from apps.sync.models import SyncDate


def onec_offline_sync(sync_data: SyncDate):
    """Load data from offline to online OneCTTN

    Args:
        sync_data (SyncDate): last sync date
    """
    if not sync_data:
        return
    offline = offline_OneCTTN.objects.filter(update_at__gt=sync_data.last_sync)
    list_ttn = []
    for i in offline:
        ttn = OneCTTN(
            id=i.id,
            number=i.number,
            series=i.series,
            create_at=i.create_at,
            update_at=i.update_at,
        )
        list_ttn.append(ttn)
        i.delete()
    OneCTTN.objects.bulk_create(list_ttn)


def onec_ttn_item_sync(sync_data: SyncDate):
    """Load data from offline to online OneCTTNItem
    """
    if not sync_data:
        return
    offline = offline_OneCTTItem.objects.select_related('onec_ttn').filter(update_at__gt=sync_data.last_sync)
    list_ttn_item = []
    for i in offline:
        ttn_item = OneCTTNItem(
            id=i.id,
            onec_ttn_id=i.onec_ttn.id,
            name=i.name,
            count=i.count,
            create_at=i.create_at,
            update_at=i.update_at,
        )
        list_ttn_item.append(ttn_item)
        i.delete()
    OneCTTNItem.objects.bulk_create(list_ttn_item)


class OneCFullSync:
    def __init__(self):
        self.sync_date = SyncDate.objects.order_by('-last_sync').first()
        if not self.sync_date:
            last_models = OfflineModels.objects.order_by('id').last()
            sync_date = SyncDate.objects.create()
            sync_date.last_sync = last_models.update_at if last_models else datetime.datetime(2000, 1, 1)
            sync_date.save()
            self.sync_date = sync_date

    def full_sync(self) -> dict:
        time_full = dict()
        time_ttn = self.onec_ttn_full_sync()
        time_item = self.onec_ttn_item_full_sync()
        time_full['ttn'] = time_ttn
        time_full['ttn_item'] = time_item
        time_full['full'] = time_ttn + time_item
        return time_full

    def onec_ttn_full_sync(self) -> float:
        start_time = time.time()
        onec_offline_sync(self.sync_date)
        offline_OneCTTN.objects.all().delete()
        onec_ttn = OneCTTN.objects.all()
        for i in onec_ttn:
            offline_OneCTTN.objects.create(
                id=i.id,
                number=i.number,
                series=i.series,
                created_at=i.created_at,
                updated_at=i.updated_at,
            )
        stop_time = time.time()
        return stop_time - start_time

    def onec_ttn_item_full_sync(self) -> float:
        start_time = time.time()
        onec_ttn_item_sync(self.sync_date)
        offline_OneCTTItem.objects.all().delete()
        onec_ttn_items = OneCTTNItem.objects.select_related('onec_ttn').all()
        for i in onec_ttn_items:
            offline_OneCTTItem.objects.create(
                id=i.id,
                onec_ttn_id=i.onec_ttn_id,
                name=i.name,
                count=i.count,
                created_at=i.created_at,
                updated_at=i.updated_at,
            )
        stop_time = time.time()
        return stop_time - start_time


class OneCSync:
    def __init__(self):
        self.sync_date = SyncDate.objects.order_by('-last_sync').first()
        if not self.sync_date:
            last_models = OfflineModels.objects.order_by('id').last()
            sync_date = SyncDate.objects.create()
            sync_date.last_sync = last_models.update_at if last_models else datetime.datetime(2000, 1, 1)
            sync_date.save()
            self.sync_date = sync_date

    def sync(self) -> dict:
        time_full = dict()
        time_ttn = self.onec_ttn_sync()
        time_item = self.onec_ttn_item_sync()
        time_full['ttn'] = time_ttn
        time_full['ttn_item'] = time_item
        time_full['full'] = time_ttn + time_item
        return time_full

    def onec_ttn_sync(self) -> float:
        start_time = time.time()
        onec_offline_sync(self.sync_date)
        onec_tnn = OneCTTN.objects.filter(update_at__gt=self.sync_date.last_sync)
        for i in onec_tnn:
            if offline_OneCTTN.objects.filter(id=i.id).exists():
                offline_OneCTTN.objects.filter(id=i.id).update(
                    number=i.number,
                    series=i.series,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                )
            else:
                offline_OneCTTN.objects.create(
                    id=i.id,
                    number=i.number,
                    series=i.series,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                )
        stop_time = time.time()
        return stop_time - start_time

    def onec_ttn_item_sync(self) -> float:
        start_time = time.time()
        onec_ttn_item_sync(self.sync_date)
        onec_ttn_item = OneCTTNItem.objects.filter(update_at__gt=self.sync_date.last_sync)
        for i in onec_ttn_item:
            if offline_OneCTTItem.objects.filter(id=i.id).exists():
                offline_OneCTTItem.objects.filter(id=i.id).update(
                    onec_ttn_id=i.onec_ttn_id,
                    name=i.name,
                    count=i.count,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                )
            else:
                offline_OneCTTItem.objects.create(
                    id=i.id,
                    onec_ttn_id=i.onec_ttn_id,
                    name=i.name,
                    count=i.count,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                )
        stop_time = time.time()
        return stop_time - start_time
