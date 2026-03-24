from rest_framework import serializers

from apps.aonec.models import OfflineOneCTTNItem
from apps.ashtrih.serializers.model import OfflineModelsSerializer


class OfflineOneCTTNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineOneCTTNItem
        fields = "__all__"


class OfflineOneCTTNItemListSerializer(serializers.ModelSerializer):
    model = OfflineModelsSerializer(read_only=True)

    class Meta:
        model = OfflineOneCTTNItem
        fields = [
            'model',
            'count'
        ]
