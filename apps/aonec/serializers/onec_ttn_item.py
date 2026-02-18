from rest_framework import serializers

from apps.aonec.models import OneCTTNItem


class OneCTTNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTNItem
        fields = "__all__"


class OneCTTNItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTNItem
        fields = [
            'name',
            'count'
        ]
