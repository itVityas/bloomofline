from rest_framework import serializers

from apps.shtrih.models import ModelNames


class ModelNamesSerializer(serializers.ModelSerializer):
    """
    Serializer for the ModelNames model.

    Handles serialization/deserialization of product model names including:
    - Full model names
    - Shortened model name abbreviations

    Fields:
        - id: Primary key identifier
        - name: Full model name (max_length=100)
        - short_name: Abbreviated model name (max_length=50)
    """
    class Meta:
        model = ModelNames
        fields = '__all__'


class CountSerializer(serializers.Serializer):
    """
    Generic count serializer for returning aggregated data with associated codes.

    Commonly used for:
    - Product counts by model/category
    - Inventory level reporting
    - Statistical aggregations

    Fields:
        - count: Integer representing the counted items
        - code: Identifier or classification code for the count
    """
    count = serializers.IntegerField()
    code = serializers.IntegerField()
