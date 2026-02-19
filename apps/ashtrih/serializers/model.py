from rest_framework import serializers

from apps.ashtrih.models import Models
from apps.ashtrih.serializers.model_name import ModelNamesSerializer


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
    name = ModelNamesSerializer(read_only=True)

    class Meta:
        model = Models
        fields = ['__all__']
