from django.db import models

from apps.ashtrih.models import OfflineModelNames


class OfflineStorageLimits(models.Model):
    """
    Defines storage time limitations for products based on production codes and models.

    Attributes:
        max_storage_days (int): Maximum allowed storage duration in days
        production_code (int): Reference to production code
        model_code (int, optional): Specific model code if limitation is model-specific

    Meta:
        ordering: Default ordering by descending ID
        verbose_name: Human-readable name for admin interface
        indexes: Database indexes for performance
    """
    max_storage_days = models.IntegerField()
    production_code = models.IntegerField()
    model_code = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        app_label = "osgp"

    def __str__(self):
        return f"StorageLimit #{self.id} (Code: {self.production_code})"


class OfflineShipmentBans(models.Model):
    """
    Tracks shipment restrictions/bans with multiple filtering criteria.

    Attributes:
        order_number: Reference order number
        order_date: Date when restriction was ordered
        message: Optional descriptive message
        date_ranges: Various date filters for the ban
        references: Optional foreign keys to related models
        is_active: Flag for active/inactive bans
        apply_to_belarus: Belarus-specific applicability

    Meta:
        ordering: Default ordering by descending ID
        verbose_name: Human-readable name for admin interface
        indexes: Database indexes for performance
    """
    order_number = models.CharField(max_length=10)
    order_date = models.DateField()
    message = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    production_code = models.IntegerField(null=True, blank=True)
    model_name_id = models.ForeignKey(
        OfflineModelNames,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        db_constraint=False)
    barcode = models.CharField(max_length=18, blank=True, null=True)
    color_code = models.CharField(max_length=4, null=True, blank=True)
    module_id = models.IntegerField(null=True, blank=True)
    shift = models.CharField(max_length=3, blank=True, null=True)
    assembly_date_from = models.DateField(blank=True, null=True)
    assembly_date_to = models.DateField(blank=True, null=True)
    pakaging_date_from = models.DateField(blank=True, null=True)
    pakaging_date_to = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    apply_to_belarus = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        app_label = "osgp"

    def __str__(self):
        return f"ShipmentBan #{self.id} ({self.order_number})"
