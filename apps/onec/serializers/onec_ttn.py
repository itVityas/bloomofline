from rest_framework import serializers

from apps.onec.models import OneCTTN, OneCTTNItem
from apps.onec.serializers.onec_ttn_item import (
    OneCTTNItemSerializer, OneCTTNItemListSerializer)


class OneCTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTN
        fields = "__all__"


class OneCTTNGetSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = OneCTTN
        fields = "__all__"

    def get_items(self, obj) -> dict:
        items = OneCTTNItem.objects.filter(onec_ttn=obj)
        return OneCTTNItemSerializer(items, many=True).data


class OneCTTNFullSerializer(serializers.ModelSerializer):
    items = OneCTTNItemListSerializer(many=True, write_only=True)

    class Meta:
        model = OneCTTN
        fields = [
            'number',
            'series',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', None)
        ttn = OneCTTN.objects.update_or_create(**validated_data)

        for item in items_data:
            OneCTTNItem.objects.update_or_create(onec_ttn=ttn[0], **item)

        return ttn[0]
