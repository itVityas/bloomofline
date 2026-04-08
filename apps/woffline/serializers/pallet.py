from rest_framework import serializers

from apps.woffline.models import OfflinePallet
from apps.ashtrih.models import OfflineProducts
from apps.woffline.utils.generate_barcode import generate_barcode
from apps.woffline.models import OfflineWarehouseTTN
from apps.ashtrih.serializers.products import OfflineProductGetSerializer


class OfflinePalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflinePallet
        exclude = ['is_offline']


class OfflinePalletGenerateSerializer(serializers.ModelSerializer):
    """barcode: 5: model + 2: month + 2: year + 3: col + 8: ttn_number
    """
    ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = OfflinePallet
        exclude = ['is_offline']

    def create(self, validated_data):
        ttn_number = validated_data.pop('ttn_number', None)
        if not ttn_number:
            raise serializers.ValidationError('Не указан номер ТТН')

        barcode = generate_barcode(ttn_number=ttn_number)
        if barcode.find('Error') != -1 or not isinstance(barcode, str):
            raise serializers.ValidationError('Не удалось сгенерировать штрих-код' + barcode)

        pallet = OfflinePallet.objects.filter(barcode=barcode).first()
        if pallet:
            return pallet

        warehouse_ttn = OfflineWarehouseTTN.objects.filter(ttn_number=ttn_number).first()
        if not warehouse_ttn:
            raise serializers.ValidationError('ТТН не найден')
        if warehouse_ttn.is_close:
            raise serializers.ValidationError('ТТН уже закрыт')
        warehouse_ttn.is_close = True
        warehouse_ttn.save()

        return OfflinePallet.objects.create(
            barcode=barcode,
            ttn_number=warehouse_ttn,
        )


class OfflinePalletProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_products')

    class Meta:
        model = OfflinePallet
        fields = ['id', 'barcode', 'ttn_number', 'products', 'create_at', 'update_at']

    def get_products(self, obj) -> dict:
        products = OfflineProducts.objects.filter(offlinewarehousedo__warehouse_ttn__ttn_number=obj.ttn_number)
        return OfflineProductGetSerializer(products, many=True).data


class OfflinePalletDecomposeSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    quantity = serializers.IntegerField()
    ttn_number = serializers.CharField()
    pallet = serializers.DictField()

    class Meta:
        fields = ['model_name', 'month', 'year', 'quantity', 'ttn_number', 'pallet']
