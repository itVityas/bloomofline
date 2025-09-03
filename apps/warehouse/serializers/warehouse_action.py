from rest_framework import serializers

from apps.warehouse.models import WarehouseAction
from apps.warehouse.serializers.type_of_work import TypeOfWorkSerializer


class WarehouseActionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseAction
        fields = "__all__"


class WarehouseActionGetSerializer(serializers.ModelSerializer):
    type_of_work = TypeOfWorkSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseAction
        fields = "__all__"
