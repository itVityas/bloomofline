from rest_framework import serializers

from apps.ashtrih.models import OfflineProducts
from apps.ashtrih.serializers.model import OfflineModelsSerializer


class OfflineProductGetSerializer(serializers.ModelSerializer):
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
    model = OfflineModelsSerializer(read_only=True)

    class Meta:
        model = OfflineProducts
        fields = '__all__'
