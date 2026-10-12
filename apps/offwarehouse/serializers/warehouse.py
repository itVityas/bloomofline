from rest_framework import serializers

from apps.offwarehouse.models import OfflineWarehouse


class OfflineWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouse
        fields = "__all__"
