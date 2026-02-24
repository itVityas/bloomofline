import time

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


class ShtrihFullSync:
    def __init__(self):
        self.sync_date = SyncDate.objects.order_by('-last_sync').first()

    def full_sync(self) -> dict:
        time_full = dict()
        time_names = self.model_names_full_sync()
        time_model = self.models_full_sync()
        time_products = self.products_full_sync()
        time_full['names'] = time_names
        time_full['models'] = time_model
        time_full['products'] = time_products
        time_full['full'] = time_names + time_model + time_products
        return time_full

    def model_names_full_sync(self) -> float:
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

    def models_full_sync(self) -> float:
        time_start = time.time()
        AshtrihModels.objects.all().delete()
        models = Models.objects.all()
        list_models = []
        for i in models:
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
        AshtrihModels.objects.bulk_create(list_models)
        time_stop = time.time()
        return time_stop - time_start

    def products_full_sync(self) -> float:
        time_start = time.time()
        AshtrihProducts.objects.all().delete()
        products = Products.objects.all()
        list_products = []
        buf = 0
        for i in products:
            buf += 1
            list_products.append(AshtrihProducts(
                id=i.id,
                model_id=i.model.id,
                barcode=i.barcode,
                state=i.state,
                quantity=i.quantity,
            ))
            if buf == 100000:
                AshtrihProducts.objects.bulk_create(list_products)
                list_products.clear()
                buf = 0
        AshtrihProducts.objects.bulk_create(list_products)
        time_stop = time.time()
        return time_stop - time_start


class ShtrihSync:
    def __init__(self):
        self.sync_date = SyncDate.objects.order_by('-last_sync').first()

    def sync(self) -> dict:
        time_full = dict()
        time_names = self.model_names_sync()
        time_model = self.models_sync()
        time_products = self.product_sync()
        time_full['names'] = time_names
        time_full['models'] = time_model
        time_full['products'] = time_products
        time_full['full'] = time_names + time_model + time_products
        return time_full

    def model_names_sync(self) -> float:
        time_start = time.time()
        last_model_name = AshtrihModelNames.objects.order_by('id').last()
        model_names = ModelNames.objects.filter(id__gt=last_model_name.id)
        for i in model_names:
            if AshtrihModelNames.objects.filter(id=i.id).exists():
                AshtrihModelNames.objects.filter(id=i.id).update(
                    name=i.name,
                    short_name=i.short_name,
                )
            else:
                AshtrihModelNames.objects.create(
                    id=i.id,
                    name=i.name,
                    short_name=i.short_name,
                )
        time_stop = time.time()
        return time_stop - time_start

    def models_sync(self) -> float:
        time_start = time.time()
        models = Models.objects.filter(update_at__gt=self.sync_date.last_sync)
        for i in models:
            if AshtrihModels.objects.filter(code=i.code).exists():
                AshtrihModels.objects.filter(code=i.code).update(
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
                AshtrihModels.objects.create(
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
        time_stop = time.time()
        return time_stop - time_start

    def product_sync(self) -> float:
        time_start = time.time()
        last_product = AshtrihProducts.objects.order_by('id').last()
        products = Products.objects.filter(id__gt=last_product.id)
        for i in products:
            if AshtrihProducts.objects.filter(id=i.id).exists():
                AshtrihProducts.objects.filter(id=i.id).update(
                    model_id=i.model.id,
                    barcode=i.barcode,
                    state=i.state,
                    quantity=i.quantity,
                )
            else:
                AshtrihProducts.objects.create(
                    id=i.id,
                    model_id=i.model.id,
                    barcode=i.barcode,
                    state=i.state,
                    quantity=i.quantity,
                )
        time_stop = time.time()
        return time_stop - time_start
