from rest_framework import serializers

from apps.warehouse.models import WarehouseTTN, WarehouseDo
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_action import WarehouseActionGetSerializer
from apps.account.serializers.user import UserSerializer
from apps.shtrih.serializers.products import ProductGetSerializer


class WarehouseTTNPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseTTN
        fields = [
            'ttn_number',
            'is_close',
            'date',
            'warehouse',
            'warehouse_action',
            'user',
            'onec_ttn'
        ]


class WarehouseTTNGetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseTTN
        fields = '__all__'


class WarehouseDoTTNSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(many=False)

    class Meta:
        model = WarehouseDo
        fields = '__all__'


class WarehouseTTNProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)
    warehousedo = serializers.SerializerMethodField()

    class Meta:
        model = WarehouseTTN
        fields = '__all__'

    def get_warehousedo(self, obj) -> list:
        warehouse_do = WarehouseDo.objects.filter(warehouse_ttn=obj)
        return WarehouseDoTTNSerializer(warehouse_do, many=True).data
