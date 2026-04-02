from rest_framework import serializers

from apps.woffline.models import (
    OfflineWarehouseDo,
    OfflineWarehouseTTN,
    OfflinePallet,
    OfflineWarehouseAction
)
from apps.ashtrih.models import OfflineProducts
from apps.ashtrih.serializers.products import OfflineProductGetSerializer
from apps.woffline.serializers.warehouse_ttn import OfflineWarehouseTTNGetSerializer
from apps.woffline.utils.generate_barcode import generate_barcode
from apps.woffline.exceptions.barcode import WrongModel


class OfflineWarehouseDoGetSerializer(serializers.ModelSerializer):
    warehouse_ttn = OfflineWarehouseTTNGetSerializer(read_only=True)
    product = OfflineProductGetSerializer(many=False, read_only=True)

    class Meta:
        model = OfflineWarehouseDo
        fields = '__all__'


class OfflineWarehouseDoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouseDo
        fields = [
            'warehouse_ttn',
            'product',
            'old_product',
            'quantity',
        ]


class OfflineWarehouseDoBarcodeSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    model_name_id = serializers.IntegerField(write_only=True, required=True)

    warehouse_ttn = OfflineWarehouseTTNGetSerializer(read_only=True)
    product = OfflineProductGetSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = OfflineWarehouseDo
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

        warehouse_action = OfflineWarehouseAction.objects.get(id=warehouse_action_id)
        if not warehouse_action or warehouse_action.type_of_work.id == 2 or warehouse_action.type_of_work.id == 3:
            raise serializers.ValidationError('Эта операция ну доступна для операций типа Отгрузка и Палетирование')

        # получает ttn
        warehouse_ttn = OfflineWarehouseTTN.objects.filter(ttn_number=number).first()
        if not warehouse_ttn:
            warehouse_ttn = OfflineWarehouseTTN.objects.create(
                ttn_number=number,
                date=date,
                warehouse_id=warehouse_id,
                warehouse_action_id=warehouse_action_id,
                user=user
            )

        # получаем или создаем warehouse product
        product = OfflineProducts.objects.filter(
            barcode=barcode
        ).first()
        if product:
            if model_name_id != product.model.name.id:
                raise WrongModel()
        else:
            raise serializers.ValidationError('Продукт не найден')

        # проверка на дублирование в ttn
        if OfflineWarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn, product=product).exists():
            raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

        warehouse_do = OfflineWarehouseDo.objects.create(
            product=product,
            warehouse_ttn=warehouse_ttn,
            quantity=quantity
        )

        return warehouse_do
