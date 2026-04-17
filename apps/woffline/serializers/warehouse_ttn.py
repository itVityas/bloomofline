from rest_framework import serializers

from apps.woffline.models import OfflineWarehouseTTN, OfflineWarehouseDo
from apps.woffline.serializers.warehouse import OfflineWarehouseSerializer
from apps.woffline.serializers.warehouse_action import OfflineWarehouseActionGetSerializer
from apps.aoffline.serializers.user import OfflineUserSerializer
from apps.ashtrih.serializers.products import OfflineProductGetSerializer


class OfflineWarehouseTTNVisibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouseTTN
        fields = [
            'ttn_number',
            'is_close',
            'date',
            'warehouse',
            'warehouse_action',
            'onec_ttn',
        ]


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
            'onec_ttn',
        ]


class OfflineWarehouseTTNGetSerializer(serializers.ModelSerializer):
    user = OfflineUserSerializer(read_only=True, many=False)
    warehouse = OfflineWarehouseSerializer(read_only=True, many=False)
    warehouse_action = OfflineWarehouseActionGetSerializer(read_only=True, many=False)

    class Meta:
        model = OfflineWarehouseTTN
        fields = '__all__'


class OfflineWarehouseDoTTNSerializer(serializers.ModelSerializer):
    product = OfflineProductGetSerializer(many=False)

    class Meta:
        model = OfflineWarehouseDo
        fields = '__all__'


class OfflineWarehouseTTNProductSerializer(serializers.ModelSerializer):
    user = OfflineUserSerializer(read_only=True, many=False)
    warehouse = OfflineWarehouseSerializer(read_only=True, many=False)
    warehouse_action = OfflineWarehouseActionGetSerializer(read_only=True, many=False)
    warehousedo = serializers.SerializerMethodField()

    class Meta:
        model = OfflineWarehouseTTN
        fields = '__all__'

    def get_warehousedo(self, obj) -> list:
        warehouse_do = OfflineWarehouseDo.objects.filter(warehouse_ttn=obj)
        return OfflineWarehouseDoTTNSerializer(warehouse_do, many=True).data
