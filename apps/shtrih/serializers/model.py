from rest_framework import serializers

from apps.shtrih.models import Models
from apps.shtrih.serializers.model_name import ModelNamesSerializer
from apps.shtrih.serializers.production_code import ProductionCodeSerializer


class ModelsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Models entity representing product specifications.

    Handles serialization of complete product model data including:
    - Technical specifications
    - Warranty information
    - Identification codes
    - Related model names and production codes

    Includes nested serializers for:
    - production_code (ProductionCodeSerializer)
    - name (ModelNamesSerializer)
    """
    omega_model_id = serializers.IntegerField()
    omega_variant_id = serializers.IntegerField()
    production_code = ProductionCodeSerializer(read_only=True)
    code = serializers.IntegerField()
    name = ModelNamesSerializer(read_only=True)
    diagonal = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_warranty = serializers.IntegerField()
    storage_warranty = serializers.IntegerField()
    variant_code = serializers.CharField(max_length=20)
    design_code = serializers.CharField(max_length=20)
    letter_part = serializers.CharField(max_length=25)
    numeric_part = serializers.CharField(max_length=20)
    execution_part = serializers.CharField(max_length=10)
    create_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()

    class Meta:
        model = Models
        fields = [
            'id',
            'omega_model_id',
            'omega_variant_id',
            'production_code',
            'code',
            'name',
            'diagonal',
            'weight',
            'quantity',
            'product_warranty',
            'storage_warranty',
            'variant_code',
            'design_code',
            'letter_part',
            'numeric_part',
            'execution_part',
            'create_at',
            'update_at',
        ]
