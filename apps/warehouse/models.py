from django.db import models

from apps.shtrih.models import Products
from apps.account.models import User
from apps.onec.models import OneCTTN


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class TypeOfWork(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class WarehouseAction(models.Model):
    name = models.CharField(max_length=100)
    type_of_work = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str(self):
        return f'{self.id}:{self.name}'


class Pallet(models.Model):
    barcode = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}:{self.barcode}'


class WarehouseProduct(models.Model):
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        db_constraint=False)
    quantity = models.PositiveIntegerField(default=1)
    is_shipment = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class WarehouseTTN(models.Model):
    ttn_number = models.CharField(max_length=50, primary_key=True)
    is_close = models.BooleanField(default=False)
    date = models. DateField(null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    warehouse_action = models.ForeignKey(WarehouseAction, on_delete=models.PROTECT)
    pallet = models.ForeignKey(Pallet, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ttn_number']

    def __str__(self):
        return f'{self.ttn_number}'


class WarehouseDo(models.Model):
    warehouse_ttn = models.ForeignKey(WarehouseTTN, on_delete=models.PROTECT)
    warehouse_product = models.ForeignKey(WarehouseProduct, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'


class Shipment(models.Model):
    onec_ttn = models.ForeignKey(OneCTTN, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    warehouse_product = models.ForeignKey(WarehouseProduct, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'
