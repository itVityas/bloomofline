from rest_framework import serializers
from django.db import transaction

from apps.warehouse.models import (
    WarehouseDo,
    WarehouseTTN,
    WarehouseAction
)
from apps.onec.models import OneCTTN, OneCTTNItem
from apps.shtrih.models import Products
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.warehouse.serializers.warehouse_ttn import WarehouseTTNGetSerializer
from apps.warehouse.exceptions.barcode import WrongModel


class WarehouseDoGetSerializer(serializers.ModelSerializer):
    warehouse_ttn = WarehouseTTNGetSerializer(read_only=True)
    product = ProductGetSerializer(many=False, read_only=True)

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
        ]

    def create(self, validated_data):
        number = validated_data.pop('warehouse_ttn_number')
        date = validated_data.pop('date')
        warehouse_id = validated_data.pop('warehouse_id')
        warehouse_action_id = validated_data.pop('warehouse_action_id')
        quantity = validated_data.pop('quantity')
        barcode = validated_data.pop('barcode')
        user = self.context['request'].user

        warehouse_action = WarehouseAction.objects.get(id=warehouse_action_id)
        if not warehouse_action or warehouse_action.type_of_work.id == 2 or warehouse_action.type_of_work.id == 3:
            raise serializers.ValidationError('Эта операция ну доступна для операций типа Отгрузка и Палетирование')

        with transaction.atomic():
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
                barcode=barcode
            ).first()
            if not product:
                raise serializers.ValidationError('Продукт не найден')

            # проверка на дублирование в ttn
            if WarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn, product=product).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            warehouse_do = WarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity
            )

        return warehouse_do


class WarehouseDoPalletSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    model_name_id = serializers.IntegerField(write_only=True, required=True)

    warehouse_ttn = WarehouseTTNGetSerializer(read_only=True)
    product = ProductGetSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(required=False, default=1)
    pallet_barcode = serializers.CharField(read_only=True)

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
            'pallet_barcode',
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
        if not warehouse_action or warehouse_action.type_of_work.id != 2:
            raise serializers.ValidationError('Эта операция доступна для операций типа Палетирование')

        with transaction.atomic():
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

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            warehouse_do = WarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity
            )

        return warehouse_do


class WarehouseDoShipmentSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    onec_ttn = serializers.IntegerField(write_only=True, required=True)

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
            'onec_ttn',
        ]

    def create(self, validated_data):
        number = validated_data.pop('warehouse_ttn_number')
        date = validated_data.pop('date')
        warehouse_id = validated_data.pop('warehouse_id')
        warehouse_action_id = validated_data.pop('warehouse_action_id')
        quantity = validated_data.pop('quantity')
        barcode = validated_data.pop('barcode')
        user = self.context['request'].user
        onec_ttn_id = validated_data.pop('onec_ttn')

        warehouse_action = WarehouseAction.objects.get(id=warehouse_action_id)
        if not warehouse_action or warehouse_action.type_of_work.id != 3:
            raise serializers.ValidationError('Эта операция доступна для операций типа Отгрузка')

        onec_ttn = OneCTTN.objects.filter(id=onec_ttn_id).first()
        if not onec_ttn:
            raise serializers.ValidationError('1C TTN не найден')

        model_name_ids = OneCTTNItem.objects.filter(onec_ttn=onec_ttn).values_list('model_name', flat=True)

        with transaction.atomic():
            # получает ttn
            warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=number).first()
            if not warehouse_ttn:
                warehouse_ttn = WarehouseTTN.objects.create(
                    ttn_number=number,
                    date=date,
                    warehouse_id=warehouse_id,
                    warehouse_action_id=warehouse_action_id,
                    user_id=user.id,
                    onec_ttn=onec_ttn,
                )

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            # получаем или создаем warehouse product
            product = Products.objects.filter(
                barcode=barcode
            ).first()
            if not product:
                raise serializers.ValidationError('Продукт не найден')
            else:
                if product.model.name.id not in model_name_ids:
                    raise serializers.ValidationError('Модель не найдена в выбранной 1C накладной')
            product.is_shipment = True
            product.available_quantity -= quantity
            if product.available_quantity < 0:
                raise serializers.ValidationError('Недостаточно товара на складе ' + str(product.available_quantity))
            product.save()

            # проверка на дублирование в ttn
            if WarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn, product=product).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            warehouse_do = WarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity
            )

        return warehouse_do
