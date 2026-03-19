from django.db import models


class OfflineModelNames(models.Model):
    """
    Represents model names with their full and short versions.
    Used as a reference table for product models.
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        app_label = "ashtrih"

    def __str__(self):
        return self.name


class OfflineModels(models.Model):
    """
    Main product model containing all technical specifications and attributes.
    Relates to ModelNames and Production_codes.
    """
    code = models.IntegerField()
    name = models.ForeignKey(OfflineModelNames, on_delete=models.CASCADE)
    diagonal = models.FloatField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    product_warranty = models.IntegerField(null=True, blank=True)
    storage_warranty = models.IntegerField(null=True, blank=True)
    create_at = models.DateTimeField(null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        app_label = "ashtrih"

    def __str__(self):
        return f"{self.name} (Code: {self.code})"


class OfflineProducts(models.Model):
    """
    Individual product items with barcodes, colors, and inventory information.
    """
    barcode = models.CharField(max_length=18)
    model = models.ForeignKey(
        OfflineModels,
        on_delete=models.CASCADE,
        db_constraint=False)
    state = models.IntegerField()
    quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        app_label = "ashtrih"

    def __str__(self):
        return f"Product {self.barcode}"


class OfflineWorkplaces(models.Model):
    """
    Workplace reference table for product components.
    """
    housing = models.CharField(max_length=3, db_column='housing')
    type_of_work = models.SmallIntegerField(db_column='type_of_work_id')
    computer_number = models.CharField(max_length=2, db_column='computer_number')
    create_at = models.DateTimeField(db_column='create_at')

    class Meta:
        app_label = "ashtrih"
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}"


class OfflineProtocols(models.Model):
    """
    Protocol reference table for product components.
    """
    product = models.ForeignKey(OfflineProducts, on_delete=models.CASCADE, db_column='product_id')
    workplace = models.ForeignKey(OfflineWorkplaces, on_delete=models.CASCADE, db_column='workplace_id')
    work_date = models.DateField(db_column='work_date')

    class Meta:
        app_label = "ashtrih"
        ordering = ['-id']

    def __str__(self):
        return f"Protocol {self.id}"
