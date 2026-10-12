from rest_framework import serializers

from apps.offonec.models import OfflineOneCTTNItem
from apps.offshtrih.serializers.model_name import OfflineModelNamesSerializer


class OfflineOneCTTNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineOneCTTNItem
        fields = "__all__"


class OfflineOneCTTNItemListSerializer(serializers.ModelSerializer):
    model_name = OfflineModelNamesSerializer(read_only=True)

    class Meta:
        model = OfflineOneCTTNItem
        fields = [
            'model_name',
            'count',
            'available_quantity'
        ]
