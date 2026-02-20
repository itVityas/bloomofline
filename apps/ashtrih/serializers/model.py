from rest_framework import serializers

from apps.ashtrih.models import OfflineModels
from apps.ashtrih.serializers.model_name import OfflineModelNamesSerializer


class OfflineModelsSerializer(serializers.ModelSerializer):
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
    name = OfflineModelNamesSerializer(read_only=True)

    class Meta:
        model = OfflineModels
        fields = '__all__'
