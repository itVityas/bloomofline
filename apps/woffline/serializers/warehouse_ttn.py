from rest_framework import serializers

from apps.woffline.models import OfflineWarehouseTTN, OfflineWarehouseProduct
from apps.woffline.serializers.warehouse import OfflineWarehouseSerializer
from apps.woffline.serializers.warehouse_action import OfflineWarehouseActionGetSerializer
from apps.aoffline.serializers.user import OfflineUserSerializer
from apps.woffline.serializers.warehouse_products import OfflineWarehouseProductGetSerializer


class OfflineWarehouseTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouseTTN
        fields = [
            'ttn_number',
            'is_close',
            'date',
            'warehouse',
            'warehouse_action',
            'pallet',
            'user',
        ]


class OfflineWarehouseTTNGetSerializer(serializers.ModelSerializer):
    user = OfflineUserSerializer(read_only=True, many=False)
    warehouse = OfflineWarehouseSerializer(read_only=True, many=False)
    warehouse_action = OfflineWarehouseActionGetSerializer(read_only=True, many=False)

    class Meta:
        model = OfflineWarehouseTTN
        fields = '__all__'


class OfflineWarehouseTTNProductSerializer(serializers.ModelSerializer):
    user = OfflineUserSerializer(read_only=True, many=False)
    warehouse = OfflineWarehouseSerializer(read_only=True, many=False)
    warehouse_action = OfflineWarehouseActionGetSerializer(read_only=True, many=False)
    products = serializers.SerializerMethodField()

    class Meta:
        model = OfflineWarehouseTTN
        fields = '__all__'

    def get_products(self, obj) -> list:
        warehouse_products = OfflineWarehouseProduct.objects.filter(offlinewarehousedo__warehouse_ttn=obj)
        return OfflineWarehouseProductGetSerializer(warehouse_products, many=True).data
