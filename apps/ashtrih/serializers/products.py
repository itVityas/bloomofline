from rest_framework import serializers

from apps.ashtrih.models import Products
from apps.ashtrih.serializers.color import ColorsSerializer
from apps.ashtrih.serializers.model import ModelsSerializer


class ProductGetSerializer(serializers.ModelSerializer):
    """
    Detailed product serializer for read operations with nested relationships.

    Provides complete product information including:
    - Full product details
    - Nested color information
    - Complete model specifications

    Fields:
        - All fields from Products model
        - Expanded color_id (ColorsSerializer)
        - Expanded model (ModelsSerializer)

    Read-only Fields:
        - All fields (since this is a GET-only serializer)
    """
    color_id = ColorsSerializer(read_only=True)
    model = ModelsSerializer(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'


class ProductUpdateClearedSerializer(serializers.ModelSerializer):
    """
    Update serializer for clearing products.

    This serializer is used to update the 'cleared' field of a product.
    It allows setting the 'cleared' field to a specific value.

    Fields:
        - cleared (IntegerField): The field to be updated with the new cleared value.

    Read-only Fields:
        - All fields (since this is an update-only serializer)
    """
    class Meta:
        model = Products
        fields = ['cleared']
