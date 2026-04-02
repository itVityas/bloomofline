from rest_framework import serializers

from apps.warehouse.models import (
    WarehouseDo,
    WarehouseTTN,
    Pallet,
    WarehouseAction
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
            'old_product',
            'quantity',
        ]


class WarehouseDoBarcodeSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    model_name_id = serializers.IntegerField(write_only=True, required=True)

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
            'model_name_id',
        ]

    def create(self, validated_data):
        number = validated_data.pop('warehouse_ttn_number')
        date = validated_data.pop('date')
        warehouse_id = validated_data.pop('warehouse_id')
        warehouse_action_id = validated_data.pop('warehouse_action_id')
        model_name_id = validated_data.pop('model_name_id')
        quantity = validated_data.pop('quantity')
        barcode = validated_data.pop('barcode')
        user = self.context['request'].user

        warehouse_action = WarehouseAction.objects.get(id=warehouse_action_id)
        if not warehouse_action or warehouse_action.type_of_work.id == 2 or warehouse_action.type_of_work.id == 3:
            raise serializers.ValidationError('Эта операция ну доступна для операций типа Отгрузка и Палетирование')

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
        product = Products.objects.filter(
            barcode=barcode
        ).first()
        if product:
            if model_name_id != product.model.name.id:
                raise WrongModel()
        else:
            raise serializers.ValidationError('Продукт не найден')

        # проверка на дублирование в ttn
        if WarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn, product=product).exists():
            raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

        warehouse_do = WarehouseDo.objects.create(
            product=product,
            warehouse_ttn=warehouse_ttn,
            quantity=quantity
        )

        return warehouse_do
