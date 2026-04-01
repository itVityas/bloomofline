from rest_framework import serializers

from apps.woffline.models import OfflineWarehouseTTN
from apps.ashtrih.models import OfflineProducts
from apps.woffline.serializers.warehouse import OfflineWarehouseSerializer
from apps.woffline.serializers.warehouse_action import OfflineWarehouseActionGetSerializer
from apps.aoffline.serializers.user import OfflineUserSerializer
from apps.ashtrih.serializers.products import OfflineProductGetSerializer


class OfflineWarehouseTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouseTTN
        fields = [
            'ttn_number',
            'is_close',
            'date',
            'warehouse',
            'warehouse_action',
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
        products = OfflineProducts.objects.filter(offlinewarehousedo__warehouse_ttn=obj)
        return OfflineProductGetSerializer(products, many=True).data
