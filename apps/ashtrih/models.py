from django.db import models


class ModelNames(models.Model):
    """
    Represents model names with their full and short versions.
    Used as a reference table for product models.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'model_names'
        ordering = ['-id']
        app_label = "ashtrih"

    def __str__(self):
        return self.name


class Models(models.Model):
    """
    Main product model containing all technical specifications and attributes.
    Relates to ModelNames and Production_codes.
    """
    code = models.IntegerField()
    name = models.ForeignKey(ModelNames, on_delete=models.CASCADE, db_column='name_id')
    diagonal = models.FloatField()
    weight = models.IntegerField()
    quantity = models.IntegerField()
    product_warranty = models.IntegerField()
    storage_warranty = models.IntegerField()
    relevance = models.BooleanField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'models'
        ordering = ['-id']
        app_label = "ashtrih"

    def __str__(self):
        return f"{self.name} (Code: {self.code})"


class Products(models.Model):
    """
    Individual product items with barcodes, colors, and inventory information.
    """
    barcode = models.CharField(max_length=18)
    model = models.ForeignKey(Models, on_delete=models.CASCADE, db_column='model_id')
    state = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products'
        ordering = ['-id']
        app_label = "ashtrih"

    def __str__(self):
        return f"Product {self.barcode}"
