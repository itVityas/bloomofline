from rest_framework import serializers

from apps.warehouse.models import Shipment, Warehouse, WarehouseProduct
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_products import WarehouseProductGetSerializer
from apps.onec.serializers.onec_ttn import OneCTTNFullSerializer
from apps.account.serializers.user import UserSerializer
from apps.shtrih.models import Products
from apps.onec.models import OneCTTN


class ShipmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'warehouse',
            'warehouse_product',
            'onec_ttn',
            'user',
            'quantity',
        ]


class ShipmentGetSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_product = WarehouseProductGetSerializer(read_only=True)
    onec_ttn = OneCTTNFullSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'


class ShipmentBarcodeSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    once_ttn_id = serializers.IntegerField(write_only=True, required=True)
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_product = WarehouseProductGetSerializer(read_only=True)
    onec_ttn = OneCTTNFullSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'barcode',
            'warehouse_id',
            'once_ttn_id',
            'warehouse',
            'warehouse_product',
            'onec_ttn',
            'user',
            'quantity',
        ]

    def create(self, validated_data):
        barcode = validated_data.pop('barcode', None)
        warehouse_id = validated_data.pop('warehouse_id', None)
        onec_ttn_id = validated_data.pop('once_ttn_id', None)
        quantity = validated_data.pop('quantity', 1)
        user = self.context['request'].user

        if not barcode or not warehouse_id or not onec_ttn_id:
            raise serializers.ValidationError('Не все поля переданны')

        warehouse = Warehouse.objects.filter(id=warehouse_id).first()
        onec_ttn = OneCTTN.objects.filter(id=onec_ttn_id).first()
        if not warehouse or not onec_ttn:
            raise serializers.ValidationError('Склад или ТТН не найдены')

        if len(barcode) == 18:
            product = Products.objects.filter(barcode=barcode).first()
            if not product:
                raise serializers.ValidationError('Продукт не найден')
            warehouse_product = WarehouseProduct.objects.filter(product=product).first()
            if not warehouse_product:
                warehouse_product = WarehouseProduct.objects.create(
                    product=product,
                    quantity=quantity
                )
            warehouse_product.is_shipment = True
            warehouse_product.save()
            shipment = Shipment.objects.create(
                warehouse=warehouse,
                warehouse_product=warehouse_product,
                onec_ttn=onec_ttn,
                user=user,
                quantity=quantity
            )
            return [shipment,]
        elif len(barcode) == 19:
            raise serializers.ValidationError('старый паллет')
        elif len(barcode) == 20:
            warehouse_products = WarehouseProduct.objects.filter(warehousedo__warehouse_ttn__pallet__barcode=barcode)
            if not warehouse_products:
                raise serializers.ValidationError('Паллет не найден не найден')
            shipments = list()
            for warehouse_product in warehouse_products:
                warehouse_product.is_shipment = True
                warehouse_product.save()
                shipment = Shipment.objects.create(
                    warehouse=warehouse,
                    warehouse_product=warehouse_product,
                    onec_ttn=onec_ttn,
                    user=user,
                    quantity=quantity
                )
                shipments.append(shipment)
            return shipments
        raise serializers.ValidationError('Не удалось распознать штрих-код')
