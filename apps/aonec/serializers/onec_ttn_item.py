from rest_framework import serializers

from apps.aonec.models import OfflineOneCTTNItem


class OfflineOneCTTNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineOneCTTNItem
        fields = "__all__"


class OfflineOneCTTNItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineOneCTTNItem
        fields = [
            'name',
            'count'
        ]
