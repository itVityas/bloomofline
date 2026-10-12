from rest_framework import serializers

from apps.offwarehouse.models import OfflineWarehouseAction
from apps.offwarehouse.serializers.type_of_work import OfflineTypeOfWorkSerializer


class OfflineWarehouseActionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouseAction
        fields = "__all__"


class OfflineWarehouseActionGetSerializer(serializers.ModelSerializer):
    type_of_work = OfflineTypeOfWorkSerializer(read_only=True, many=False)

    class Meta:
        model = OfflineWarehouseAction
        fields = "__all__"
