from rest_framework import serializers

from apps.offshipment.models import OfflineOneCTTN, OfflineOneCTTNItem
from apps.offshipment.serializers.onec_ttn_item import (
    OfflineOneCTTNItemListSerializer)


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
        items = OfflineOneCTTNItem.objects.filter(onec_ttn_id=obj.id)
        return OfflineOneCTTNItemListSerializer(items, many=True).data
