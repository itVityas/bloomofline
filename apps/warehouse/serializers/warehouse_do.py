from datetime import date as datetype

from rest_framework import serializers
from django.db import transaction
from django.db.models import Q

from apps.warehouse.models import (
    WarehouseDo,
    WarehouseTTN,
    WarehouseAction,
    Pallet,
    NotPackaging,
)
from apps.onec.models import OneCTTN, OneCTTNItem
from apps.sgp.models import ShipmentBans
from apps.shtrih.models import Products, Workplaces
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

        warehouse_action = WarehouseAction.objects.get(id=warehouse_action_id, is_deleted=False)
        if not warehouse_action or warehouse_action.type_of_work.id == 2 or warehouse_action.type_of_work.id == 3:
            raise serializers.ValidationError('Эта операция не доступна для операций типа Отгрузка и Палетирование')

        # получаем или создаем warehouse product
        product = Products.objects.filter(
            barcode=barcode
        ).first()
        if not product:
            raise serializers.ValidationError('Продукт не найден')
        last_workplace = Workplaces.objects.filter(protocols__product=product).order_by('-id').first()
        if last_workplace and last_workplace.type_of_work.id != 3:
            if NotPackaging.objects.filter(product=product, is_solved=False).exists():
                NotPackaging.objects.create(
                    product=product,
                    warehouse_id=warehouse_id,
                    bloom_user_id=user.id,
                    found_date=date,
                    is_solved=False,
                    solve_date=None
                )
            raise serializers.ValidationError('Товар не прошел упаковку')

        if product.available_quantity <= 0 and not (
                    warehouse_action.type_of_work.id == 4 or warehouse_action.type_of_work.id == 1
                ):
            raise serializers.ValidationError('Доступных товаров 0 или тип операции не возврат и приход')

        # Проверка на две одинаковые операции на складе с одним и тем же штрихкодом
        last_ttn = WarehouseTTN.objects.filter(warehousedo__product=product, is_deleted=False).order_by('-date').first()
        if last_ttn.warehouse_action == warehouse_action and last_ttn.warehouse_id == warehouse_id:
            raise serializers.ValidationError('Вы не можете добавить один и тот же штрихкод дважды подряд')

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

            # проверка на дублирование в ttn
            if WarehouseDo.objects.filter(
                    warehouse_ttn=warehouse_ttn,
                    product=product,
                    is_deleted=False).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

            if warehouse_action.type_of_work == 4:
                product.is_shipment = False
                product.available_quantity += quantity
                product.save()

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

        warehouse_action = WarehouseAction.objects.get(id=warehouse_action_id, is_deleted=False)
        if not warehouse_action or warehouse_action.type_of_work.id != 2:
            raise serializers.ValidationError('Эта операция доступна для операций типа Палетирование')

        # получаем или создаем warehouse product
        product = Products.objects.filter(
            barcode=barcode
        ).first()
        if product:
            if model_name_id != product.model.name.id:
                raise WrongModel()
        else:
            raise serializers.ValidationError('Продукт не найден')
        last_workplace = Workplaces.objects.filter(protocols__product=product).order_by('-id').first()
        if last_workplace and last_workplace.type_of_work.id != 3:
            if NotPackaging.objects.filter(product=product, is_solved=False).exists():
                NotPackaging.objects.create(
                    product=product,
                    warehouse_id=warehouse_id,
                    bloom_user_id=user.id,
                    found_date=date,
                    is_solved=False,
                    solve_date=None
                )
            raise serializers.ValidationError('Товар не прошел упаковку')

        if product.available_quantity <= 0 and not (
                    warehouse_action.type_of_work.id == 4 or warehouse_action.type_of_work.id == 1
                ):
            raise serializers.ValidationError('Доступных товаров 0 или тип операции не возврат и приход')

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

            # проверка на дублирование в ttn
            if WarehouseDo.objects.filter(
                    warehouse_ttn=warehouse_ttn,
                    product=product,
                    is_deleted=False).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

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

        warehouse_action = WarehouseAction.objects.get(id=warehouse_action_id, is_deleted=False)
        if not warehouse_action or warehouse_action.type_of_work.id != 3:
            raise serializers.ValidationError('Эта операция доступна для операций типа Отгрузка')

        onec_ttn = OneCTTN.objects.filter(id=onec_ttn_id).first()
        if not onec_ttn:
            raise serializers.ValidationError('1C TTN не найден')

        model_name_ids = OneCTTNItem.objects.filter(onec_ttn=onec_ttn).values_list('model_name', flat=True)

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
        onec_item = OneCTTNItem.objects.filter(onec_ttn=onec_ttn, model_name=product.model.name).first()
        if not onec_item:
            raise serializers.ValidationError('Товары 1C накладной не найдены')
        if onec_item.available_quantity < quantity:
            raise serializers.ValidationError('Недостаточно товара в 1C накладной')
        onec_item.available_quantity -= quantity

        bans = ShipmentBans.objects.filter(
            Q(start_date=None) | Q(start_date__lt=datetype.today()),
            Q(end_date=None) | Q(end_date__gt=datetype.today()),
            Q(barcode=None) | Q(barcode=product.barcode),
            Q(production_code=None) | Q(production_code=product.model.production_code),
            Q(model_name_id=None) | Q(model_name_id=product.model.name),
            Q(color_code=None) | Q(color_code=product.color_code),
            Q(module_id=None) | Q(module_id=product.module_id),
            Q(shift=None) | Q(shift=product.shift),
            Q(pakaging_date_from=None) | Q(pakaging_date_from__lt=product.work_date),
            Q(pakaging_date_to=None) | Q(pakaging_date_to__gt=product.work_date),
            Q(apply_to_belarus=None) | Q(apply_to_belarus=onec_ttn.is_bel_receiver),
            is_active=True,
        )
        if bans:
            raise serializers.ValidationError('Товар в запрете на отгрузку: ', [i.order_number for i in bans])

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

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

            product.save()
            onec_item.save()

            # проверка на дублирование в ttn
            if WarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn, product=product, is_deleted=False).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            warehouse_do = WarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity
            )

        return warehouse_do


class WarehouseDoShipmentDeleteSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True)
    new_ttn = serializers.CharField(write_only=True)
    onec_number = serializers.CharField(write_only=True)
    onec_series = serializers.CharField(write_only=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)

    class Meta:
        model = WarehouseDo
        fields = [
            'barcode',
            'new_ttn',
            'onec_number',
            'onec_series',
            'warehouse_id',
            'warehouse_action_id',
            'date',
        ]

    def create(self, validated_data):
        barcode = validated_data.pop('barcode')
        new_ttn = validated_data.pop('new_ttn')
        onec_number = validated_data.pop('onec_number')
        onec_series = validated_data.pop('onec_series')
        user = self.context['request'].user
        date = validated_data.pop('date')
        warehouse_id = validated_data.pop('warehouse_id')
        warehouse_action_id = validated_data.pop('warehouse_action_id')

        if not barcode or not new_ttn or not onec_number or not onec_series:
            raise serializers.ValidationError('Предоставлены не все данные')
        if not user:
            raise serializers.ValidationError('Нету пользователя')

        warehouse_ttn = WarehouseTTN.objects.filter(
            onec_ttn__number=onec_number, onec_ttn__series=onec_series, is_deleted=False)
        if not warehouse_ttn:
            raise serializers.ValidationError('ТТН не найдена')
        onec_ttn = warehouse_ttn[0].onec_ttn

        warehouse_do = WarehouseDo.objects.filter(
            warehouse_ttn__in=warehouse_ttn,
            product__barcode=barcode,
            is_deleted=False
        )

        pallet = None
        if len(barcode) > 18:
            pallet = Pallet.objects.filter(barcode=barcode).first()
            warehouse_do = WarehouseDo.objects.filter(warehouse_ttn=pallet.ttn_number, is_deleted=False)

        if not warehouse_do:
            raise serializers.ValidationError('Данные не найдены')

        with transaction.atomic():
            warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=new_ttn).first()
            if not warehouse_ttn:
                warehouse_ttn = WarehouseTTN.objects.create(
                    ttn_number=new_ttn,
                    date=date,
                    warehouse_id=warehouse_id,
                    warehouse_action_id=warehouse_action_id,
                    user_id=user.id,
                    onec_ttn=onec_ttn,
                )

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

            if pallet:
                list_new_do = []
                for i in warehouse_do:
                    warehouse_do_new = WarehouseDo.objects.create(
                        product=i.product,
                        warehouse_ttn=warehouse_ttn,
                        quantity=i.quantity
                    )
                    onec_item = OneCTTNItem.objects.filter(
                        onec_ttn=onec_ttn, model_name=i.product.model.name).first()
                    onec_item.available_quantity += i.quantity
                    if onec_item.available_quantity > onec_item.count:
                        onec_item.available_quantity = onec_item.count
                    i.product.available_quantity += i.quantity
                    i.product.is_shipment = False
                    i.product.save()
                    onec_item.save()
                list_new_do.append(warehouse_do_new)
            else:
                warehouse_do_new = WarehouseDo.objects.create(
                    product=warehouse_do[0].product,
                    warehouse_ttn=warehouse_ttn,
                    quantity=warehouse_do[0].quantity
                )
                onec_item = OneCTTNItem.objects.filter(
                    onec_ttn=onec_ttn, model_name=warehouse_do[0].product.model.name).first()
                onec_item.available_quantity += warehouse_do[0].quantity
                if onec_item.available_quantity > onec_item.count:
                    onec_item.available_quantity = onec_item.count
                warehouse_do[0].product.available_quantity += warehouse_do[0].quantity
                warehouse_do[0].product.is_shipment = False
                warehouse_do[0].product.save()
                onec_item.save()
        warehouse_do.update(is_deleted=True)
        return warehouse_do_new
