from rest_framework import serializers

from apps.shtrih.models import Colors


class ColorsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Colors model.

    Handles serialization and deserialization of Color instances,
    including validation of color data.

    Fields:
        - color_code: 4-character color code (optional)
        - russian_title: Color description in Russian (optional)
    """
    class Meta:
        model = Colors
        fields = '__all__'
