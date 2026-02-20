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

    def full_sync(self):
        self.model_names_full_sync()
        self.models_full_sync()

    def model_names_full_sync():
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

    def models_full_sync(self):
        AshtrihModels.objects.all().delete()
        models = Models.objects.all()
        list_models = []
        for i in models:
            list_models.append(AshtrihModels(
                code=i.code,
                name=i.name,
                diagonal=i.diagonal,
                weight=i.weight,
                quantity=i.quantity,
                product_warranty=i.product_warranty,
                storage_warranty=i.storage_warranty,
                relevance=i.relevance,
                create_at=i.create_at,
                update_at=i.update_at,
            ))
        AshtrihModels.objects.bulk_create(list_models)

    def products_full_sync(self):
        AshtrihProducts.objects.all().delete()
        products = Products.objects.all()
        list_products = []
        for i in products:
            list_products.append(AshtrihProducts(
                id=i.id,
                model=i.model,
                number=i.number,
                price=i.price,
                currency=i.currency,
                availability=i.availability,
                create_at=i.create_at,
                update_at=i.update_at,
            ))
        AshtrihProducts.objects.bulk_create(list_products)


class ShtrihSync:
    def __init__(self):
        self.sync_date = SyncDate.objects.order_by('-last_sync').first()

    def sync(self):
        self.model_names_sync()
        self.models_sync()

    def model_names_sync(self):
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

    def models_sync(self):
        models = Models.objects.filter(update_at__gt=self.sync_date.last_sync)
        for i in models:
            if AshtrihModels.objects.filter(code=i.code).exists():
                AshtrihModels.objects.filter(code=i.code).update(
                    name=i.name,
                    diagonal=i.diagonal,
                    weight=i.weight,
                    quantity=i.quantity,
                    product_warranty=i.product_warranty,
                    storage_warranty=i.storage_warranty,
                    relevance=i.relevance,
                    create_at=i.create_at,
                    update_at=i.update_at,
                )
            else:
                AshtrihModels.objects.create(
                    code=i.code,
                    name=i.name,
                    diagonal=i.diagonal,
                    weight=i.weight,
                    quantity=i.quantity,
                    product_warranty=i.product_warranty,
                    storage_warranty=i.storage_warranty,
                    relevance=i.relevance,
                    create_at=i.create_at,
                    update_at=i.update_at,
                )

    def product_sync(self):
        last_product = AshtrihProducts.objects.order_by('id').last()
        products = Products.objects.filter(id__gt=last_product.id)
        for i in products:
            if AshtrihProducts.objects.filter(id=i.id).exists():
                AshtrihProducts.objects.filter(id=i.id).update(
                    model=i.model,
                    number=i.number,
                    price=i.price,
                    currency=i.currency,
                    availability=i.availability,
                    create_at=i.create_at,
                    update_at=i.update_at,
                )
            else:
                AshtrihProducts.objects.create(
                    id=i.id,
                    model=i.model,
                    number=i.number,
                    price=i.price,
                    currency=i.currency,
                    availability=i.availability,
                    create_at=i.create_at,
                    update_at=i.update_at,
                )
