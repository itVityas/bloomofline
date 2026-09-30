import time

from django.db import transaction, connection, connections
from django.db.models import OuterRef, Subquery
import logging


from apps.shtrih.models import (
    ModelNames,
    Models,
    Products,
    Protocols,
    Colors
)
from apps.ashtrih.models import (
    OfflineModels as AshtrihModels,
    OfflineProducts as AshtrihProducts,
    OfflineModelNames as AshtrihModelNames,
)
from apps.sync.models import SyncDate


logger = logging.getLogger(__name__)


def product_update(update_date: SyncDate = None):
    products = AshtrihProducts.objects.filter(is_offline=True)
    products_ids = []
    products_dict = {}
    for i in products:
        products_ids.append(i.id)
        products_dict[i.id] = i
    product_to_update = Products.objects.filter(id__in=products_ids)
    for i in product_to_update:
        buf = products_dict.get(i.id)
        if buf:
            i.available_quantity = buf.available_quantity
            i.is_shipment = buf.is_shipment
    Products.objects.bulk_update(product_to_update, ['available_quantity', 'is_shipment'])


class ShtrihFullSync:
    def __init__(self, sync_date: SyncDate, batch_size: int = 2000):
        self.batch_size = batch_size
        self.sync_date = sync_date

    def _iter_products_mssql(self, batch_size: int):
        sql = """
            WITH latest_protocol AS (
                SELECT product_id, MAX(id) AS max_id
                FROM protocols
                GROUP BY product_id
            )
            SELECT
                p.id, p.model_id, p.barcode, p.state, p.quantity,
                p.available_quantity, p.is_shipment,
                pr.work_date, pr.shift,
                w.type_of_work_id, w.module_id,
                c.color_code, c.russian_title
            FROM products p
            LEFT JOIN latest_protocol lp ON lp.product_id = p.id
            LEFT JOIN protocols pr      ON pr.id = lp.max_id
            LEFT JOIN workplaces w       ON w.id = pr.workplace_id
            LEFT JOIN colors c          ON c.id = p.color_id
        """
        with connections['bloom'].cursor() as cursor:
            cursor.execute(sql)
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                for row in rows:
                    yield row

    def _bulk_insert_products_from_mssql(self) -> int:
        PRODUCT_INSERT_SQL = """
        INSERT INTO ashtrih_offlineproducts
                (id, model_id, barcode, state, quantity, available_quantity,
                is_shipment, work_date, type_of_work_id, module_id,
                color_code, russian_title, shift, is_offline)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """
        batch, total = [], 0
        with connection.cursor() as sqlite_cursor:
            for row in self._iter_products_mssql(self.batch_size):
                batch.append(row)
                if len(batch) >= self.batch_size:
                    sqlite_cursor.executemany(PRODUCT_INSERT_SQL, batch)
                    total += len(batch)
                    batch.clear()
            if batch:
                sqlite_cursor.executemany(PRODUCT_INSERT_SQL, batch)
                total += len(batch)
        return total

    def full_sync(self) -> dict:
        try:
            time_full = dict()
            time_names = self.model_names_full_sync()
            time_model = self.models_full_sync()
            time_products = self.products_full_sync()
            time_full['names'] = time_names
            time_full['models'] = time_model
            time_full['products'] = time_products
            time_full['full'] = time_names + time_model + time_products
            return time_full
        except Exception as e:
            logger.error('shtrih full sync: ' + str(e))
            raise e

    def model_names_full_sync(self) -> float:
        try:
            time_start = time.time()
            model_names = ModelNames.objects.all().values('id', 'name', 'short_name')
            list_names = []
            for i in model_names:
                list_names.append(AshtrihModelNames(
                    id=i['id'],
                    name=i['name'],
                    short_name=i['short_name'],
                ))
            AshtrihModelNames.objects.bulk_create(list_names)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('model_names_full_sync: ' + str(e))
            raise e

    def models_full_sync(self) -> float:
        try:
            time_start = time.time()
            models = Models.objects.select_related('name').all().order_by('id').values(
                'id', 'code', 'name_id', 'diagonal', 'weight', 'quantity',
                'product_warranty', 'storage_warranty',
                'create_at', 'update_at', 'production_code_id')
            list_models = []
            for i in models.iterator(chunk_size=self.batch_size):
                list_models.append(AshtrihModels(
                    id=i['id'],
                    code=i['code'],
                    name_id=i['name_id'],
                    diagonal=i['diagonal'],
                    weight=i['weight'],
                    quantity=i['quantity'],
                    product_warranty=i['product_warranty'],
                    storage_warranty=i['storage_warranty'],
                    production_code=i['production_code_id'],
                    create_at=i['create_at'],
                    update_at=i['update_at'],
                ))
                if len(list_models) >= self.batch_size:
                    AshtrihModels.objects.bulk_create(list_models)
                    list_models.clear()
            if list_models:
                AshtrihModels.objects.bulk_create(list_models)
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('models_full_sync: ' + str(e))
            raise e

    def products_full_sync(self) -> float:
        try:
            time_start = time.time()
            self._bulk_insert_products_from_mssql()
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('products_full_sync: ' + str(e))
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
            logger.error('shtrih sync: ' + str(e))
            raise e

    def model_names_sync(self) -> float:
        try:
            time_start = time.time()
            last_model_name = AshtrihModelNames.objects.order_by('id').last()
            existing_ids = set(AshtrihModelNames.objects.values_list('id', flat=True))
            model_names = ModelNames.objects.filter(id__gt=last_model_name.id).order_by('id').values(
                'id', 'name', 'short_name')
            list_models = []
            list_update = []
            buf = 0
            for i in model_names.iterator(chunk_size=self.batch_size):
                buf += 1
                if i['id'] in existing_ids:
                    list_update.append(i)
                else:
                    list_models.append(AshtrihModelNames(
                        id=i['id'],
                        name=i['name'],
                        short_name=i['short_name'],
                    ))
                if buf >= self.batch_size:
                    AshtrihModelNames.objects.bulk_create(list_models)
                    list_models.clear()
                    buf = 0
            if list_models:
                AshtrihModelNames.objects.bulk_create(list_models)
            if list_update:
                for i in list_update:
                    AshtrihModelNames.objects.filter(id=i['id']).update(
                        name=i['name'],
                        short_name=i['short_name'],
                    )
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('model_names_sync: ' + str(e))
            raise e

    def models_sync(self) -> float:
        try:
            time_start = time.time()
            last_model = AshtrihModels.objects.order_by('-id').first()
            models = Models.objects.filter(id__gt=last_model.id if last_model else 0).order_by('id').values(
                'id', 'code', 'name_id', 'diagonal', 'weight', 'quantity',
                'product_warranty', 'storage_warranty',
                'create_at', 'update_at', 'production_code_id'
            )
            existing_ids = set(AshtrihModels.objects.values_list('id', flat=True))
            list_models = []
            list_update = []
            buf = 0
            for i in models.iterator(chunk_size=self.batch_size):
                buf += 1
                if i['id'] in existing_ids:
                    list_update.append(i)
                else:
                    list_models.append(AshtrihModels(
                        code=i['code'],
                        name_id=i['name_id'],
                        diagonal=i['diagonal'],
                        weight=i['weight'],
                        quantity=i['quantity'],
                        product_warranty=i['product_warranty'],
                        storage_warranty=i['storage_warranty'],
                        production_code=i['production_code_id'],
                        create_at=i['create_at'],
                        update_at=i['update_at'],
                    ))
                if buf >= self.batch_size:
                    AshtrihModels.objects.bulk_create(list_models)
                    list_models.clear()
                    buf = 0
            if list_models:
                AshtrihModels.objects.bulk_create(list_models)
            if list_update:
                for i in list_update:
                    AshtrihModels.objects.filter(id=i['id']).update(
                        code=i['code'],
                        name_id=i['name_id'],
                        diagonal=i['diagonal'],
                        weight=i['weight'],
                        quantity=i['quantity'],
                        product_warranty=i['product_warranty'],
                        storage_warranty=i['storage_warranty'],
                        create_at=i['create_at'],
                        update_at=i['update_at'],
                    )
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('models_sync: ' + str(e))
            raise e

    def product_sync(self) -> float:
        try:
            time_start = time.time()
            product_update()
            last_product = AshtrihProducts.objects.order_by('-id').first()
            latest_protocol = Protocols.objects.filter(
                product_id=OuterRef('id')
            ).order_by('-id')
            latest_work_date = Subquery(latest_protocol.values('work_date')[:1])
            shift = Subquery(latest_protocol.values('shift')[:1])
            latest_type_of_work_id = Subquery(
                latest_protocol.values('workplace__type_of_work_id')[:1]
            )
            latest_module_id = Subquery(
                latest_protocol.values('workplace__module_id')[:1]
            )
            color_subquery = Colors.objects.filter(id=OuterRef('color_id'))
            products = Products.objects.filter(
                id__gt=last_product.id if last_product else 0).annotate(
                work_date=latest_work_date,
                shift=shift,
                type_of_work_id=latest_type_of_work_id,
                module_id=latest_module_id,
                color_code=Subquery(color_subquery.values('color_code')[:1]),
                russian_title=Subquery(color_subquery.values('russian_title')[:1])
            ).order_by('id').values(
                'id', 'model_id', 'barcode', 'state', 'quantity', 'available_quantity', 'is_shipment',
                'work_date', 'type_of_work_id', 'module_id', 'color_code', 'russian_title', 'shift')
            list_products = []
            existing_ids = set(AshtrihProducts.objects.values_list('id', flat=True))
            list_products = []
            list_update = []
            for i in products.iterator(chunk_size=self.batch_size):
                if i['id'] in existing_ids:
                    list_update.append([i])
                else:
                    list_products.append(AshtrihProducts(
                        id=i['id'],
                        model_id=i['model_id'],
                        barcode=i['barcode'],
                        state=i['state'],
                        quantity=i['quantity'],
                        available_quantity=i['available_quantity'],
                        is_shipment=i['is_shipment'],
                        work_date=i['work_date'],
                        type_of_work_id=i['type_of_work_id'],
                        module_id=i['module_id'],
                        color_code=i['color_code'],
                        russian_title=i['russian_title'],
                        shift=i['shift'],
                    ))
                if len(list_products) >= self.batch_size:
                    AshtrihProducts.objects.bulk_create(list_products)
                    list_products.clear()
            if list_products:
                AshtrihProducts.objects.bulk_create(list_products)
            if list_update:
                for i in list_update:
                    AshtrihProducts.objects.filter(id=i[0]['id']).update(
                        model_id=i[0]['model_id'],
                        barcode=i[0]['barcode'],
                        state=i[0]['state'],
                        quantity=i[0]['quantity'],
                        available_quantity=i[0]['available_quantity'],
                        is_shipment=i[0]['is_shipment'],
                        work_date=i['work_date'],
                        type_of_work_id=i['type_of_work_id'],
                        module_id=i['module_id'],
                        color_code=i['color_code'],
                        russian_title=i['russian_title'],
                        shift=i['shift'],
                    )
            time_stop = time.time()
            return time_stop - time_start
        except Exception as e:
            logger.error('product_sync: ' + str(e))
            raise e
