from rest_framework import serializers

from apps.onec.models import OneCTTN, OneCTTNItem
from apps.shtrih.models import Models
from apps.onec.serializers.onec_ttn_item import (
    OneCTTNItemListSerializer, OneCTTNItemDesinerSerializer)


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
        return OneCTTNItemListSerializer(items, many=True).data


class OneCTTNFullSerializer(serializers.ModelSerializer):
    items = OneCTTNItemDesinerSerializer(many=True, write_only=True)

    class Meta:
        model = OneCTTN
        fields = [
            'number',
            'series',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', None)
        OneCTTN.objects.create(**validated_data)
        ttn = OneCTTN.objects.filter(**validated_data).first()

        for item in items_data:
            count = item.pop('count', None)
            model = Models.objects.filter(design_code=item['desiner_code']).first()
            if not count or not model:
                raise serializers.ValidationError('no model or count')
            OneCTTNItem.objects.create(onec_ttn=ttn, count=count, model=model)

        return ttn
