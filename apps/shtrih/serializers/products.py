from rest_framework import serializers

from apps.shtrih.models import Products
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.serializers.model import ModelsSerializer


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
