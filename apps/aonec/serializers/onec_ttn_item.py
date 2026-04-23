from rest_framework import serializers

from apps.aonec.models import OfflineOneCTTNItem
from apps.ashtrih.serializers.model_name import OfflineModelNamesSerializer


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
