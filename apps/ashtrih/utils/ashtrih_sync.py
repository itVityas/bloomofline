import time

from django.db import transaction
import logging


from apps.shtrih.models import (
    ModelNames,
    Models,
    Products,
)
from apps.ashtrih.models import (
    OfflineModels as AshtrihModels,
    OfflineProducts as AshtrihProducts,
    OfflineModelNames as AshtrihModelNames,
)
from apps.sync.models import SyncDate


logger = logging.getLogger(__name__)


class ShtrihFullSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.batch_size = batch_size
        self.sync_date = sync_date

    def full_sync(self) -> dict:
        try:
            time_full = dict()
            with transaction.atomic():
                time_names = self.model_names_full_sync()
                time_model = self.models_full_sync()
                time_products = self.products_full_sync()
            time_full['names'] = time_names
            time_full['models'] = time_model
            time_full['products'] = time_products
            time_full['full'] = time_names + time_model + time_products
            return time_full
        except Exception as e:
            raise e

    def model_names_full_sync(self) -> float:
        try:
            time_start = time.time()
            AshtrihModelNames.objects.all().delete()
            model_names = ModelNames.objects.all()
            list_names = []
            for i in model_names:
                list_names.append(AshtrihModelNames(
                    id=i.id,
                    name=i.name,
                    short_name=i.short_name,
                ))
            AshtrihModelNames.objects.bulk_create(list_names)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('model_names_full_sync' + str(e))
            raise e

    def models_full_sync(self) -> float:
        try:
            time_start = time.time()
            AshtrihModels.objects.all().delete()
            models = Models.objects.select_related('name').all().order_by('id')
            list_models = []
            for i in models.iterator(chunk_size=self.batch_size):
                list_models.append(AshtrihModels(
                    code=i.code,
                    name_id=i.name.id,
                    diagonal=i.diagonal,
                    weight=i.weight,
                    quantity=i.quantity,
                    product_warranty=i.product_warranty,
                    storage_warranty=i.storage_warranty,
                    create_at=i.create_at,
                    update_at=i.update_at,
                ))
                if len(list_models) >= self.batch_size:
                    AshtrihModels.objects.bulk_create(list_models)
                    list_models.clear()
            if list_models:
                AshtrihModels.objects.bulk_create(list_models)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('models_full_sync' + str(e))
            raise e

    def products_full_sync(self) -> float:
        try:
            time_start = time.time()
            AshtrihProducts.objects.all().delete()
            products = Products.objects.select_related('model').all().order_by('id')
            list_products = []
            buf = 0
            for i in products.iterator(chunk_size=self.batch_size):
                buf += 1
                list_products.append(AshtrihProducts(
                    id=i.id,
                    model_id=i.model.id,
                    barcode=i.barcode,
                    state=i.state,
                    quantity=i.quantity,
                ))
                if len(list_products) >= self.batch_size:
                    AshtrihProducts.objects.bulk_create(list_products)
                    list_products.clear()
            if list_products:
                AshtrihProducts.objects.bulk_create(list_products)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('products_full_sync' + str(e))
            raise e


class ShtrihSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 1000):
        self.sync_date = sync_date
        self.batch_size = batch_size

    def sync(self) -> dict:
        try:
            with transaction.atomic():
                time_full = dict()
                time_names = self.model_names_sync()
                time_model = self.models_sync()
                time_products = self.product_sync()
                time_full['names'] = time_names
                time_full['models'] = time_model
                time_full['products'] = time_products
                time_full['full'] = time_names + time_model + time_products
                return time_full
        except Exception as e:
            raise e

    def model_names_sync(self) -> float:
        try:
            time_start = time.time()
            last_model_name = AshtrihModelNames.objects.order_by('id').last()
            existing_ids = set(AshtrihModelNames.objects.values_list('id', flat=True))
            model_names = ModelNames.objects.filter(id__gt=last_model_name.id).order_by('id')
            list_models = []
            for i in model_names.iterator(chunk_size=self.batch_size):
                if i.id in existing_ids:
                    AshtrihModelNames.objects.filter(id=i.id).update(
                        name=i.name,
                        short_name=i.short_name,
                    )
                else:
                    list_models.append(AshtrihModelNames(
                        id=i.id,
                        name=i.name,
                        short_name=i.short_name,
                    ))
                if len(list_models) >= self.batch_size:
                    AshtrihModelNames.objects.bulk_create(list_models)
                    list_models.clear()
            if list_models:
                AshtrihModelNames.objects.bulk_create(list_models)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('model_names_sync' + str(e))
            raise e

    def models_sync(self) -> float:
        try:
            time_start = time.time()
            last_model = AshtrihModels.objects.order_by('-id').first()
            models = Models.objects.filter(id__gt=last_model.id if last_model else 0).order_by('id')
            existing_ids = set(AshtrihModels.objects.values_list('id', flat=True))
            list_models = []
            for i in models.iterator(chunk_size=self.batch_size):
                if i.id in existing_ids:
                    AshtrihModels.objects.filter(id=i.id).update(
                        code=i.code,
                        name_id=i.name.id,
                        diagonal=i.diagonal,
                        weight=i.weight,
                        quantity=i.quantity,
                        product_warranty=i.product_warranty,
                        storage_warranty=i.storage_warranty,
                        create_at=i.create_at,
                        update_at=i.update_at,
                    )
                else:
                    list_models.append(AshtrihModels(
                        code=i.code,
                        name_id=i.name.id,
                        diagonal=i.diagonal,
                        weight=i.weight,
                        quantity=i.quantity,
                        product_warranty=i.product_warranty,
                        storage_warranty=i.storage_warranty,
                        create_at=i.create_at,
                        update_at=i.update_at,
                    ))
                if len(list_models) >= self.batch_size:
                    AshtrihModels.objects.bulk_create(list_models)
                    list_models.clear()
            if list_models:
                AshtrihModels.objects.bulk_create(list_models)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('models_sync' + str(e))
            raise e

    def product_sync(self) -> float:
        try:
            time_start = time.time()
            last_product = AshtrihProducts.objects.order_by('-id').first()
            products = Products.objects.filter(id__gt=last_product.id if last_product else 0).order_by('id').values(
                'id', 'model_id', 'barcode', 'state', 'quantity'
            )
            existing_ids = set(AshtrihProducts.objects.values_list('id', flat=True))
            list_products = []
            for i in products.iterator(chunk_size=self.batch_size):
                if i['id'] in existing_ids:
                    AshtrihProducts.objects.filter(id=i.id).update(
                        model_id=i.model.id,
                        barcode=i.barcode,
                        state=i.state,
                        quantity=i.quantity,
                    )
                else:
                    list_products.append(AshtrihProducts(
                        id=i['id'],
                        model_id=i['model_id'],
                        barcode=i['barcode'],
                        state=i['state'],
                        quantity=i['quantity'],
                    ))
                if len(list_products) >= self.batch_size:
                    print(len(list_products))
                    AshtrihProducts.objects.bulk_create(list_products)
                    list_products.clear()
            if list_products:
                AshtrihProducts.objects.bulk_create(list_products)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('product_sync' + str(e))
            raise e
