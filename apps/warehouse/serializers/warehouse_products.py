from rest_framework import serializers

from apps.warehouse.models import (
    WarehouseProduct,
    WarehouseDo,
    WarehouseTTN
)
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.shtrih.models import Products, Protocols
from apps.warehouse.exceptions.barcode import (
    ProductNotFound, PaсkagingNotFound)


class WarehouseProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = [
            'product',
            'quantity',
        ]


class WarehouseProductGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseProduct
        fields = "__all__"


class WarehouseProductBarcodeSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True)
    check_packaging = serializers.BooleanField(write_only=True, default=False)
    number = serializers.CharField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = WarehouseProduct
        fields = [
            'barcode',
            'quantity',
            'check_packaging',
            'number',
            'date',
            'warehouse_id',
            'warehouse_action_id',
        ]
        extra_kwargs = {
            'product': {'read_only': True},
        }

    def validate_barcode(self, value):
        if not Products.objects.filter(barcode=value).exists():
            raise ProductNotFound()
        return value

    def create(self, validated_data):
        barcode = validated_data.pop('barcode')
        product = Products.objects.get(barcode=barcode)
        check_packaging = validated_data.pop('check_packaging', False)
        number = validated_data.pop('number', None)
        date = validated_data.pop('date', None)
        warehouse_id = validated_data.pop('warehouse_id', None)
        warehouse_action_id = validated_data.pop('warehouse_action_id', None)
        user = self.context['request'].user

        if not number or not date or not warehouse_id or not warehouse_action_id:
            raise serializers.ValidationError(
                'Не указаны обязательные поля: number, date, warehouse_id, warehouse_action_id')
        warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=number).first()
        if not warehouse_ttn:
            warehouse_ttn = WarehouseTTN.objects.create(
                ttn_number=number,
                date=date,
                warehouse_id=warehouse_id,
                warehouse_action_id=warehouse_action_id,
                user=user
            )

        if product:
            if check_packaging:
                is_packaging = Protocols.objects.\
                    filter(product=product).\
                    filter(workplace__type_of_work=3).\
                    exists()
                if not is_packaging:
                    raise PaсkagingNotFound()
        else:
            ProductNotFound()

        if not validated_data.get('quantity', None):
            validated_data['quantity'] = product.quantity
        quantity = validated_data.get("quantity", 1)

        warehouse_product = WarehouseProduct.objects.create(
            product=product,
            **validated_data
        )
        WarehouseDo.objects.create(
            warehouse_product=warehouse_product,
            warehouse_ttn=warehouse_ttn,
            user=user,
            quantity=quantity
        )
        return warehouse_product
