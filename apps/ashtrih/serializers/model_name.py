from rest_framework import serializers

from apps.ashtrih.models import OfflineModelNames, OfflineModels


class OfflineModelNamesSerializer(serializers.ModelSerializer):
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
        model = OfflineModelNames
        fields = '__all__'


class OfflineModelNamesCodeSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for model names focusing on code-based identification.

    This serializer is optimized for:
    - Fast API responses
    - Code lookups and references
    - Reduced data transfer overhead

    Fields:
        - id: Primary key
        - code: Model identification code
    """
    code = serializers.SerializerMethodField(method_name='get_code')

    class Meta:
        model = OfflineModelNames
        fields = ('id', 'name', 'short_name', 'code')

    def get_code(self, obj) -> int:
        model = OfflineModels.objects.filter(name=obj).first()
        return model.code if model else 0


class OfflineCountSerializer(serializers.Serializer):
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
