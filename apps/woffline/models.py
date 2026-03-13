from django.db import models

from apps.ashtrih.models import OfflineProducts
from apps.aoffline.models import OfflineUser
from apps.aonec.models import OfflineOneCTTN


class OfflineWarehouse(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class OfflineTypeOfWork(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class OfflineWarehouseAction(models.Model):
    name = models.CharField(max_length=100)
    type_of_work = models.ForeignKey(OfflineTypeOfWork, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['id']

    def __str(self):
        return f'{self.id}:{self.name}'


class OfflinePallet(models.Model):
    barcode = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_offline = models.BooleanField(default=True)

    class Meta:
        app_label = "woffline"
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}:{self.barcode}'


class OfflineWarehouseProduct(models.Model):
    product = models.ForeignKey(
        OfflineProducts,
        on_delete=models.CASCADE,
        db_constraint=False)
    quantity = models.PositiveIntegerField(default=1)
    is_shipment = models.BooleanField(default=False)
    is_offline = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['-id']


class OfflineWarehouseTTN(models.Model):
    ttn_number = models.CharField(max_length=50, primary_key=True)
    is_close = models.BooleanField(default=False)
    is_offline = models.BooleanField(default=True)
    date = models. DateField(null=True, blank=True)
    warehouse = models.ForeignKey(OfflineWarehouse, on_delete=models.CASCADE)
    warehouse_action = models.ForeignKey(OfflineWarehouseAction, on_delete=models.CASCADE)
    pallet = models.ForeignKey(OfflinePallet, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(OfflineUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['-ttn_number']

    def __str__(self):
        return f'{self.ttn_number}'


class OfflineWarehouseDo(models.Model):
    warehouse_ttn = models.ForeignKey(OfflineWarehouseTTN, on_delete=models.CASCADE)
    warehouse_product = models.ForeignKey(OfflineWarehouseProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(OfflineUser, on_delete=models.CASCADE)
    is_offline = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'


class OfflineShipment(models.Model):
    onec_ttn = models.ForeignKey(OfflineOneCTTN, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(OfflineWarehouse, on_delete=models.CASCADE)
    warehouse_product = models.ForeignKey(OfflineWarehouseProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_offline = models.BooleanField(default=True)
    user = models.ForeignKey(OfflineUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "woffline"
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'


class OfflineOldProduct(models.Model):
    """
    Individual old_product items with barcodes, colors, and inventory information.
    """
    barcode = models.CharField(max_length=18)
    # color_id = models.ForeignKey(
    #     'ashtrih.Colors',
    #     on_delete=models.CASCADE,
    #     db_column='color_id',
    #     db_constraint=False,
    #     null=True,
    #     blank=True)
    model = models.ForeignKey(
        'ashtrih.OfflineModels',
        on_delete=models.CASCADE,
        db_column='model_id',
        db_constraint=False)
    state = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        ordering = ['-id']
        app_label = "woffline"

    def __str__(self):
        return f"old_product {self.id} {self.barcode}"
