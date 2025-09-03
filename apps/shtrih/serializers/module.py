from rest_framework import serializers

from apps.shtrih.models import Modules


class ModulesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Modules model representing product components/modules.

    Handles serialization and deserialization of module data including:
    - Module identification numbers
    - Digit codes

    Fields:
        - id: Auto-generated primary key
        - number: Module identification number
        - digit: Module classification digit
    """
    class Meta:
        model = Modules
        fields = '__all__'
