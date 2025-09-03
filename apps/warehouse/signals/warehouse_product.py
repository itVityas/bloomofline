from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.warehouse.models import WarehouseProduct, WarehouseProductHistory


@receiver(post_save, sender=WarehouseProduct)
def WarehouseProductSignal(sender, instance, created, **kwargs):
    if instance:
        WarehouseProductHistory.objects.create(
            warehouse_product=instance,
            product=instance.product,
            warehouse=instance.warehouse,
            warehouse_action=instance.warehouse_action,
            user=instance.user,
            warehouse_ttn=instance.warehouse_ttn,
            quantity=instance.quantity,
            ttn_number=instance.ttn_number,
            date=instance.date,
            create_at=instance.create_at,
            update_at=instance.update_at
        )
