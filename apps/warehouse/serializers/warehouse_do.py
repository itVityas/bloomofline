from rest_framework import serializers

from apps.warehouse.models import (
    WarehouseDo,
    WarehouseProduct,
    WarehouseTTN,
    Pallet
)
from apps.shtrih.models import Products
from apps.warehouse.serializers.warehouse_products import WarehouseProductGetSerializer
from apps.warehouse.serializers.warehouse_ttn import WarehouseTTNGetSerializer
from apps.warehouse.utils.generate_barcode import generate_barcode
from apps.warehouse.exceptions.barcode import WrongModel


class WarehouseDoGetSerializer(serializers.ModelSerializer):
    warehouse_ttn = WarehouseTTNGetSerializer(read_only=True)
    warehouse_product = WarehouseProductGetSerializer(many=False, read_only=True)

    class Meta:
        model = WarehouseDo
        fields = '__all__'


class WarehouseDoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseDo
        fields = [
            'warehouse_ttn',
            'warehouse_product',
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
    warehouse_product = WarehouseProductGetSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = WarehouseDo
        fields = [
            'warehouse_ttn',
            'warehouse_product',
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
                user=user
            )

        # получаем или создаем warehouse product
        warehouse_product = WarehouseProduct.objects.filter(
            product__barcode=barcode
        ).first()
        if warehouse_product:
            if model_id != warehouse_product.product.model.id:
                raise WrongModel()
        else:
            product = Products.objects.filter(barcode=barcode).first()
            if not product:
                raise serializers.ValidationError('Продукт не найден')
            if model_id != product.model.id:
                raise WrongModel()
            warehouse_product = WarehouseProduct.objects.create(
                product=product,
                quantity=quantity
            )

        warehouse_do = WarehouseDo.objects.create(
            warehouse_product=warehouse_product,
            warehouse_ttn=warehouse_ttn,
            user=user,
            quantity=quantity
        )

        # проверяем палет в ттн
        if not warehouse_ttn.pallet:
            pallet_barcode = generate_barcode(number)
            if pallet_barcode.find('Error') != -1 or not isinstance(pallet_barcode, str):
                raise serializers.ValidationError('Не удалось сгенерировать штрих-код' + pallet_barcode)
            pallet = Pallet.objects.create(barcode=pallet_barcode)
            warehouse_ttn.pallet = pallet
            warehouse_ttn.save()

        return warehouse_do
