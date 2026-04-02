from rest_framework import serializers

from apps.warehouse.models import WarehouseTTN
from apps.shtrih.models import Products
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_action import WarehouseActionGetSerializer
from apps.account.serializers.user import UserSerializer
from apps.shtrih.serializers.products import ProductGetSerializer


class WarehouseTTNPostSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

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


class WarehouseTTNProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)
    products = serializers.SerializerMethodField()

    class Meta:
        model = WarehouseTTN
        fields = '__all__'

    def get_products(self, obj) -> list:
        products = Products.objects.filter(warehousedo__warehouse_ttn=obj)
        return ProductGetSerializer(products, many=True).data
