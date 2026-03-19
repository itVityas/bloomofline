from rest_framework import serializers

from apps.woffline.models import OfflineShipment, OfflineWarehouse, OfflineWarehouseProduct
from apps.woffline.serializers.warehouse import OfflineWarehouseSerializer
from apps.woffline.serializers.warehouse_products import OfflineWarehouseProductGetSerializer
from apps.aonec.serializers.onec_ttn import OfflineOneCTTNFullSerializer
from apps.aoffline.serializers.user import OfflineUserSerializer
from apps.ashtrih.models import OfflineProducts
from apps.aonec.models import OfflineOneCTTN


class OfflineShipmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineShipment
        fields = [
            'warehouse',
            'warehouse_product',
            'onec_ttn',
            'user',
            'quantity',
        ]


class OfflineShipmentGetSerializer(serializers.ModelSerializer):
    warehouse = OfflineWarehouseSerializer(read_only=True)
    warehouse_product = OfflineWarehouseProductGetSerializer(read_only=True)
    onec_ttn = OfflineOneCTTNFullSerializer(read_only=True)
    user = OfflineUserSerializer(read_only=True)

    class Meta:
        model = OfflineShipment
        fields = '__all__'


class OfflineShipmentBarcodeSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    once_ttn_id = serializers.IntegerField(write_only=True, required=True)
    warehouse = OfflineWarehouseSerializer(read_only=True)
    warehouse_product = OfflineWarehouseProductGetSerializer(read_only=True)
    onec_ttn = OfflineOneCTTNFullSerializer(read_only=True)

    class Meta:
        model = OfflineShipment
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

        warehouse = OfflineWarehouse.objects.filter(id=warehouse_id).first()
        onec_ttn = OfflineOneCTTN.objects.filter(id=onec_ttn_id).first()
        if not warehouse or not onec_ttn:
            raise serializers.ValidationError('Склад или ТТН не найдены')

        if len(barcode) == 18:
            product = OfflineProducts.objects.filter(barcode=barcode).first()
            if not product:
                raise serializers.ValidationError('Продукт не найден')
            warehouse_product = OfflineWarehouseProduct.objects.filter(product=product).first()
            if not warehouse_product:
                warehouse_product = OfflineWarehouseProduct.objects.create(
                    product=product,
                    quantity=quantity
                )
            warehouse_product.is_shipment = True
            warehouse_product.save()
            shipment = OfflineShipment.objects.create(
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
            warehouse_products = OfflineWarehouseProduct.objects.filter(
                warehousedo__warehouse_ttn__pallet__barcode=barcode)
            if not warehouse_products:
                raise serializers.ValidationError('Паллет не найден не найден')
            shipments = list()
            for warehouse_product in warehouse_products:
                warehouse_product.is_shipment = True
                warehouse_product.save()
                shipment = OfflineShipment.objects.create(
                    warehouse=warehouse,
                    warehouse_product=warehouse_product,
                    onec_ttn=onec_ttn,
                    user=user,
                    quantity=quantity
                )
                shipments.append(shipment)
            return shipments
        raise serializers.ValidationError('Не удалось распознать штрих-код')
