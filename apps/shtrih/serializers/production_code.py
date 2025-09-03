from rest_framework import serializers

from apps.shtrih.models import Production_codes


class ProductionCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for Production Codes representing manufacturing identifiers.

    Handles serialization and validation of production code information including:
    - Unique production codes
    - Descriptive names
    - Nameplate indicators

    Fields:
        - code: Primary key production code (integer)
        - name: Descriptive name of production code (max 70 chars)
        - nameplate: Boolean indicating if nameplate is required
    """
    class Meta:
        model = Production_codes
        fields = '__all__'
