from rest_framework import serializers

from apps.warehouse.models import (
    Pallet,
)
from apps.shtrih.models import Products
from apps.warehouse.utils.generate_barcode import generate_barcode
from apps.warehouse.models import WarehouseTTN
from apps.shtrih.serializers.products import ProductGetSerializer


class PalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = "__all__"


class PalletGenerateSerializer(serializers.ModelSerializer):
    """barcode: 5: model + 2: month + 2: year + 3: col + 8: ttn_number
    """
    ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Pallet
        fields = "__all__"

    def create(self, validated_data):
        ttn_number = validated_data.pop('ttn_number', None)
        if not ttn_number:
            raise serializers.ValidationError('Не указан номер ТТН')

        barcode = generate_barcode(ttn_number=ttn_number)
        if barcode.find('Error') != -1 or not isinstance(barcode, str):
            raise serializers.ValidationError('Не удалось сгенерировать штрих-код' + barcode)

        pallet = Pallet.objects.filter(barcode=barcode).first()
        if pallet:
            return pallet

        warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
        if not warehouse_ttn:
            raise serializers.ValidationError('ТТН не найден')
        if warehouse_ttn.is_close:
            raise serializers.ValidationError('ТТН уже закрыт')
        warehouse_ttn.is_close = True
        warehouse_ttn.save()

        return Pallet.objects.create(
            barcode=barcode,
            ttn_number=warehouse_ttn,
        )


class PalletProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_products')

    class Meta:
        model = Pallet
        fields = ['id', 'barcode', 'ttn_number', 'products', 'create_at', 'update_at']

    def get_products(self, obj) -> dict:
        products = Products.objects.filter(warehousedo__warehouse_ttn__ttn_number=obj.ttn_number)
        return ProductGetSerializer(products, many=True).data


class PalletDecomposeSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    quantity = serializers.IntegerField()
    ttn_number = serializers.CharField()
    pallet = serializers.DictField()

    class Meta:
        fields = ['model_name', 'month', 'year', 'quantity', 'ttn_number', 'pallet']
