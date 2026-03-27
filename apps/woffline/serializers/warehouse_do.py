from rest_framework import serializers

from apps.woffline.models import (
    OfflineWarehouseDo,
    OfflineWarehouseProduct,
    OfflineWarehouseTTN,
    OfflinePallet
)
from apps.ashtrih.models import OfflineProducts
from apps.woffline.serializers.warehouse_products import OfflineWarehouseProductGetSerializer
from apps.woffline.serializers.warehouse_ttn import OfflineWarehouseTTNGetSerializer
from apps.woffline.utils.generate_barcode import generate_barcode
from apps.woffline.exceptions.barcode import WrongModel


class OfflineWarehouseDoGetSerializer(serializers.ModelSerializer):
    warehouse_ttn = OfflineWarehouseTTNGetSerializer(read_only=True)
    warehouse_product = OfflineWarehouseProductGetSerializer(many=False, read_only=True)

    class Meta:
        model = OfflineWarehouseDo
        fields = '__all__'


class OfflineWarehouseDoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineWarehouseDo
        fields = [
            'warehouse_ttn',
            'warehouse_product',
            'quantity',
            'user',
        ]


class OfflineWarehouseDoPalletSerializer(serializers.ModelSerializer):
    warehouse_ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(write_only=True, required=True)
    warehouse_id = serializers.IntegerField(write_only=True, required=True)
    warehouse_action_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True)
    model_id = serializers.IntegerField(write_only=True, required=True)

    warehouse_ttn = OfflineWarehouseTTNGetSerializer(read_only=True)
    warehouse_product = OfflineWarehouseProductGetSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = OfflineWarehouseDo
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
        warehouse_product = OfflineWarehouseProduct.objects.filter(
            product__barcode=barcode
        ).first()
        if warehouse_product:
            if model_id != warehouse_product.product.model.id:
                raise WrongModel()
        else:
            product = OfflineProducts.objects.filter(barcode=barcode).first()
            if not product:
                raise serializers.ValidationError('Продукт не найден')
            if model_id != product.model.id:
                raise WrongModel()
            warehouse_product = OfflineWarehouseProduct.objects.create(
                product=product,
                quantity=quantity
            )

        warehouse_do = OfflineWarehouseDo.objects.create(
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
            pallet = OfflinePallet.objects.create(barcode=pallet_barcode)
            warehouse_ttn.pallet = pallet
            warehouse_ttn.save()

        return warehouse_do
