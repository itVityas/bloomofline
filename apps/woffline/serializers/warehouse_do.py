from datetime import date as datetype

from rest_framework import serializers
from django.db import transaction
from django.db.models import Q

from apps.woffline.models import (
    OfflineWarehouseDo,
    OfflineWarehouseTTN,
    OfflineWarehouseAction,
    OfflinePallet,
    OfflineNotPackaging,
)
from apps.aonec.models import OfflineOneCTTN, OfflineOneCTTNItem
from apps.ashtrih.models import OfflineProducts
from apps.osgp.models import OfflineShipmentBans
from apps.ashtrih.serializers.products import OfflineProductGetSerializer
from apps.woffline.serializers.warehouse_ttn import OfflineWarehouseTTNGetSerializer
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
        ]

    def create(self, validated_data):
        number = validated_data.pop('warehouse_ttn_number')
        date = validated_data.pop('date')
        warehouse_id = validated_data.pop('warehouse_id')
        warehouse_action_id = validated_data.pop('warehouse_action_id')
        quantity = validated_data.pop('quantity')
        barcode = validated_data.pop('barcode')
        user = self.context['request'].user

        warehouse_action = OfflineWarehouseAction.objects.get(id=warehouse_action_id, is_deleted=False)
        if not warehouse_action or warehouse_action.type_of_work.id == 2 or warehouse_action.type_of_work.id == 3:
            raise serializers.ValidationError('Эта операция не доступна для операций типа Отгрузка и Палетирование')

        # получаем или создаем warehouse product
        product = OfflineProducts.objects.filter(
            barcode=barcode
        ).first()
        if not product:
            raise serializers.ValidationError('Продукт не найден')
        if product.type_of_work_id != 3:
            if not OfflineNotPackaging.objects.filter(product=product, is_solved=False).exists():
                OfflineNotPackaging.objects.create(
                    product=product,
                    warehouse_id=warehouse_id,
                    bloom_user_id=user.id,
                    found_date=date,
                    is_solved=False,
                    is_offline=True,
                    solve_date=None
                )
            raise serializers.ValidationError('Товар не прошел Упаковку')

        if product.available_quantity <= 0 and not (
                    warehouse_action.type_of_work.id == 4 or warehouse_action.type_of_work.id == 1
                ):
            raise serializers.ValidationError('Доступных товаров 0 или тип операции не возврат и приход')

        # Проверка на две одинаковые операции на складе с одним и тем же штрихкодом
        last_ttn = OfflineWarehouseTTN.objects.filter(
            offlinewarehousedo__product=product,
            is_deleted=False).order_by('-date').first()
        if last_ttn.warehouse_action == warehouse_action and last_ttn.warehouse_id == warehouse_id:
            raise serializers.ValidationError('Вы не можете добавить один и тот же штрихкод дважды подряд')

        with transaction.atomic():
            # получает ttn
            warehouse_ttn = OfflineWarehouseTTN.objects.filter(ttn_number=number).first()
            if not warehouse_ttn:
                warehouse_ttn = OfflineWarehouseTTN.objects.create(
                    ttn_number=number,
                    date=date,
                    warehouse_id=warehouse_id,
                    warehouse_action_id=warehouse_action_id,
                    user_id=user.id,
                    is_close=False,
                    is_deleted=False,
                    is_offline=True
                )

            # проверка на дублирование в ttn
            if OfflineWarehouseDo.objects.filter(
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
                product.is_offline = True
                product.save()

            warehouse_do = OfflineWarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity,
                is_deleted=False,
                is_offline=True
            )

        return warehouse_do


class OfflineWarehouseDoPalletSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    model_name_id = serializers.IntegerField(write_only=True, required=True)

    warehouse_ttn = OfflineWarehouseTTNGetSerializer(read_only=True)
    product = OfflineProductGetSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(required=False, default=1)
    pallet_barcode = serializers.CharField(read_only=True)

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

        warehouse_action = OfflineWarehouseAction.objects.get(id=warehouse_action_id, is_deleted=False)
        if not warehouse_action or warehouse_action.type_of_work.id != 2:
            raise serializers.ValidationError('Эта операция доступна для операций типа Палетирование')

        # получаем или создаем warehouse product
        product = OfflineProducts.objects.filter(
            barcode=barcode
        ).first()
        if product:
            if model_name_id != product.model.name.id:
                raise WrongModel()
        else:
            raise serializers.ValidationError('Продукт не найден')
        if product.type_of_work_id != 3:
            if not OfflineNotPackaging.objects.filter(product=product, is_solved=False).exists():
                OfflineNotPackaging.objects.create(
                    product=product,
                    warehouse_id=warehouse_id,
                    bloom_user_id=user.id,
                    found_date=date,
                    is_solved=False,
                    is_offline=True,
                    solve_date=None
                )
            raise serializers.ValidationError('Товар не прошел Упаковку')

        if product.available_quantity <= 0 and not (
                    warehouse_action.type_of_work.id == 4 or warehouse_action.type_of_work.id == 1
                ):
            raise serializers.ValidationError('Доступных товаров 0 или тип операции не возврат и приход')

        with transaction.atomic():
            # получает ttn
            warehouse_ttn = OfflineWarehouseTTN.objects.filter(ttn_number=number).first()
            if not warehouse_ttn:
                warehouse_ttn = OfflineWarehouseTTN.objects.create(
                    ttn_number=number,
                    date=date,
                    warehouse_id=warehouse_id,
                    warehouse_action_id=warehouse_action_id,
                    user_id=user.id,
                    is_close=False,
                    is_deleted=False,
                    is_offline=True
                )

            # проверка на дублирование в ttn
            if OfflineWarehouseDo.objects.filter(
                    warehouse_ttn=warehouse_ttn,
                    product=product,
                    is_deleted=False).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

            warehouse_do = OfflineWarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity,
                is_offline=True,
                is_deleted=False
            )

        return warehouse_do


class OfflineWarehouseDoShipmentSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    onec_ttn = serializers.IntegerField(write_only=True, required=True)

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

        warehouse_action = OfflineWarehouseAction.objects.get(id=warehouse_action_id, is_deleted=False)
        if not warehouse_action or warehouse_action.type_of_work.id != 3:
            raise serializers.ValidationError('Эта операция доступна для операций типа Отгрузка')

        onec_ttn = OfflineOneCTTN.objects.filter(id=onec_ttn_id).first()
        if not onec_ttn:
            raise serializers.ValidationError('1C TTN не найден')

        model_name_ids = OfflineOneCTTNItem.objects.filter(onec_ttn=onec_ttn).values_list('model_name_id', flat=True)

        # получаем или создаем warehouse product
        product = OfflineProducts.objects.filter(
            barcode=barcode
        ).first()
        if not product:
            raise serializers.ValidationError('Продукт не найден')
        else:
            if product.model.name.id not in model_name_ids:
                raise serializers.ValidationError('Модель не найдена в выбранной 1C накладной')
        product.is_shipment = True
        product.is_offline = True
        product.available_quantity -= quantity
        if product.available_quantity < 0:
            raise serializers.ValidationError('Недостаточно товара на складе ' + str(product.available_quantity))
        onec_item = OfflineOneCTTNItem.objects.filter(onec_ttn=onec_ttn, model_name=product.model.name).first()
        if not onec_item:
            raise serializers.ValidationError('Товары 1C накладной не найдены')
        if onec_item.available_quantity < quantity:
            raise serializers.ValidationError('Недостаточно товара в 1C накладной')
        onec_item.available_quantity -= quantity
        onec_item.is_offline = True

        bans = OfflineShipmentBans.objects.filter(
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
            warehouse_ttn = OfflineWarehouseTTN.objects.filter(ttn_number=number).first()
            if not warehouse_ttn:
                warehouse_ttn = OfflineWarehouseTTN.objects.create(
                    ttn_number=number,
                    date=date,
                    warehouse_id=warehouse_id,
                    warehouse_action_id=warehouse_action_id,
                    user_id=user.id,
                    onec_ttn=onec_ttn,
                    is_close=False,
                    is_deleted=False,
                    is_offline=True
                )

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

            product.save()
            onec_item.save()

            # проверка на дублирование в ttn
            if OfflineWarehouseDo.objects.filter(
                        warehouse_ttn=warehouse_ttn,
                        product=product,
                        is_deleted=False
                    ).exists():
                raise serializers.ValidationError('Продукт уже добавлен в эту ТТН')

            warehouse_do = OfflineWarehouseDo.objects.create(
                product=product,
                warehouse_ttn=warehouse_ttn,
                quantity=quantity,
                is_offline=True,
                is_deleted=False
            )

        return warehouse_do


class OfflineWarehouseDoShipmentDeleteSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True)
    new_ttn = serializers.CharField(write_only=True)
    onec_number = serializers.CharField(write_only=True)
    onec_series = serializers.CharField(write_only=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)

    class Meta:
        model = OfflineWarehouseDo
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

        warehouse_ttn = OfflineWarehouseTTN.objects.filter(
            onec_ttn__number=onec_number, onec_ttn__series=onec_series, is_deleted=False).first()
        if not warehouse_ttn:
            raise serializers.ValidationError('Warehouse ТТН не найдена')
        onec_ttn = warehouse_ttn.onec_ttn

        warehouse_do = OfflineWarehouseDo.objects.filter(
            warehouse_ttn=warehouse_ttn,
            product__barcode=barcode,
            is_deleted=False
        )

        pallet = None
        if len(barcode) > 18:
            pallet = OfflinePallet.objects.filter(barcode=barcode).first()
            warehouse_do = OfflineWarehouseDo.objects.filter(
                warehouse_ttn=pallet.ttn_number, is_deleted=False)

        if not warehouse_do:
            raise serializers.ValidationError('Данные не найдены')

        with transaction.atomic():
            warehouse_ttn = OfflineWarehouseTTN.objects.filter(ttn_number=new_ttn).first()
            if not warehouse_ttn:
                warehouse_ttn = OfflineWarehouseTTN.objects.create(
                    ttn_number=new_ttn,
                    date=date,
                    warehouse_id=warehouse_id,
                    warehouse_action_id=warehouse_action_id,
                    user_id=user.id,
                    onec_ttn=onec_ttn,
                    is_close=False,
                    is_deleted=False,
                    is_offline=True
                )

            if warehouse_ttn.is_close:
                raise serializers.ValidationError('ТТН уже закрыто')

            if warehouse_ttn.is_deleted:
                raise serializers.ValidationError('ТТН уже удалено')

            if pallet:
                list_new_do = []
                for i in warehouse_do:
                    warehouse_do_new = OfflineWarehouseDo.objects.create(
                        product=i.product,
                        warehouse_ttn=warehouse_ttn,
                        quantity=i.quantity,
                        is_offline=True,
                        is_deleted=False
                    )
                    onec_item = OfflineOneCTTNItem.objects.filter(
                        onec_ttn=onec_ttn, model_name=i.product.model.name).first()
                    onec_item.available_quantity += i.quantity
                    onec_item.is_offline = True
                    if onec_item.available_quantity > onec_item.count:
                        onec_item.available_quantity = onec_item.count
                    i.product.available_quantity += i.quantity
                    i.product.is_shipment = False
                    i.product.is_offline = True
                    i.product.save()
                    onec_item.save()
                list_new_do.append(warehouse_do_new)
            else:
                warehouse_do_new = OfflineWarehouseDo.objects.create(
                    product=warehouse_do[0].product,
                    warehouse_ttn=warehouse_ttn,
                    quantity=warehouse_do[0].quantity,
                    is_offline=True,
                    is_deleted=False
                )
                onec_item = OfflineOneCTTNItem.objects.filter(
                    onec_ttn=onec_ttn, model_name=warehouse_do[0].product.model.name).first()
                onec_item.available_quantity += warehouse_do[0].quantity
                onec_item.is_offline = True
                if onec_item.available_quantity > onec_item.count:
                    onec_item.available_quantity = onec_item.count
                warehouse_do[0].product.available_quantity += warehouse_do[0].quantity
                warehouse_do[0].product.is_shipment = False
                warehouse_do[0].product.is_offline = True
                warehouse_do[0].product.save()
                onec_item.save()
        warehouse_do.update(is_deleted=True, is_offline=True)
        return warehouse_do_new
