from rest_framework import serializers

from apps.warehouse.models import (
    WarehouseDo,
    WarehouseTTN,
    Pallet
)
from apps.shtrih.models import Products
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.warehouse.serializers.warehouse_ttn import WarehouseTTNGetSerializer
from apps.warehouse.utils.generate_barcode import generate_barcode
from apps.warehouse.exceptions.barcode import WrongModel


class WarehouseDoGetSerializer(serializers.ModelSerializer):
    warehouse_ttn = WarehouseTTNGetSerializer(read_only=True)
    warehouse_product = ProductGetSerializer(many=False, read_only=True)

    class Meta:
        model = WarehouseDo
        fields = '__all__'


class WarehouseDoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseDo
        fields = [
            'warehouse_ttn',
            'product',
            'quantity',
        ]


class WarehouseDoPalletSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    model_id = serializers.IntegerField(write_only=True, required=True)

    warehouse_ttn = WarehouseTTNGetSerializer(read_only=True)
    product = ProductGetSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = WarehouseDo
        fields = [
            'warehouse_ttn',
            'product',
            'quantity',
            'warehouse_ttn_number',
            'barcode',
            'date',
            'warehouse_id',
            'warehouse_action_id',
            'model_id',
        ]

    def create(self, validated_data):
        number = validated_data.pop('warehouse_ttn_number')
        date = validated_data.pop('date')
        warehouse_id = validated_data.pop('warehouse_id')
        warehouse_action_id = validated_data.pop('warehouse_action_id')
        model_id = validated_data.pop('model_id')
        quantity = validated_data.pop('quantity')
        barcode = validated_data.pop('barcode')
        user = self.context['request'].user

        # получает ttn
        warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=number).first()
        if not warehouse_ttn:
            warehouse_ttn = WarehouseTTN.objects.create(
                ttn_number=number,
                date=date,
                warehouse_id=warehouse_id,
                warehouse_action_id=warehouse_action_id,
                user_id=user.id
            )

        # получаем или создаем warehouse product
        product = Products.objects.filter(
            product__barcode=barcode
        ).first()
        if product:
            if model_id != product.model.id:
                raise WrongModel()
        else:
            raise serializers.ValidationError('Продукт не найден')

        warehouse_do = WarehouseDo.objects.create(
            product=product,
            warehouse_ttn=warehouse_ttn,
            quantity=quantity
        )

        # проверяем палет в ттн
        # if not warehouse_ttn.pallet:
        #     pallet_barcode = generate_barcode(number)
        #     if pallet_barcode.find('Error') != -1 or not isinstance(pallet_barcode, str):
        #         raise serializers.ValidationError('Не удалось сгенерировать штрих-код' + pallet_barcode)
        #     Pallet.objects.create(barcode=pallet_barcode, ttn_number=warehouse_ttn)

        return warehouse_do
