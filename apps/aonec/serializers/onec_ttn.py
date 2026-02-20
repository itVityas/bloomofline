from rest_framework import serializers

from apps.aonec.models import OfflineOneCTTN, OfflineOneCTTNItem
from apps.aonec.serializers.onec_ttn_item import (
    OfflineOneCTTNItemSerializer, OfflineOneCTTNItemListSerializer)


class OfflineOneCTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineOneCTTN
        fields = "__all__"


class OfflineOneCTTNGetSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = OfflineOneCTTN
        fields = "__all__"

    def get_items(self, obj) -> dict:
        items = OfflineOneCTTNItem.objects.filter(onec_ttn=obj)
        return OfflineOneCTTNItemSerializer(items, many=True).data


class OfflineOneCTTNFullSerializer(serializers.ModelSerializer):
    items = OfflineOneCTTNItemListSerializer(many=True, write_only=True)

    class Meta:
        model = OfflineOneCTTN
        fields = [
            'number',
            'series',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', None)
        ttn = OfflineOneCTTN.objects.update_or_create(**validated_data)

        for item in items_data:
            OfflineOneCTTNItem.objects.update_or_create(onec_ttn=ttn[0], **item)

        return ttn[0]
