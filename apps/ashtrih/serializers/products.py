from datetime import date

from rest_framework import serializers

from apps.ashtrih.models import OfflineProducts
from apps.ashtrih.serializers.model import OfflineModelsSerializer
from apps.shtrih.serializers.model import ModelsSerializer
from apps.shtrih.models import Products, Protocols


class OfflineProductGetSerializer(serializers.ModelSerializer):
    """
    Detailed product serializer for read operations with nested relationships.

    Provides complete product information including:
    - Full product details
    - Nested color information
    - Complete model specifications

    Fields:
        - All fields from Products model
        - Expanded color_id (ColorsSerializer)
        - Expanded model (ModelsSerializer)

    Read-only Fields:
        - All fields (since this is a GET-only serializer)
    """
    model = OfflineModelsSerializer(read_only=True)

    class Meta:
        model = OfflineProducts
        fields = '__all__'


class OnlineProductGetSerializer(serializers.ModelSerializer):
    model = ModelsSerializer
    type_of_work_id = serializers.SerializerMethodField(method_name='get_type_of_work_id')
    work_date = serializers.SerializerMethodField(method_name='get_work_date')
    module_id = serializers.SerializerMethodField(method_name='get_module_id')
    color_code = serializers.SerializerMethodField(method_name='get_color_code')
    russian_title = serializers.SerializerMethodField(method_name='get_russian_title')

    class Meta:
        model = Products
        fields = [
            'id',
            'barcode',
            'model',
            'state',
            'quantity',
            'type_of_work_id',
            'work_date',
            'module_id',
            'color_code',
            'russian_title',
        ]

    def get_type_of_work_id(self, obj) -> int:
        protocols = Protocols.objects.select_related('workplace').filter(product=obj).order_by('-work_date').first()
        if protocols:
            return protocols.workplace.type_of_work_id
        return None

    def get_work_date(self, obj) -> date:
        protocols = Protocols.objects.filter(product=obj).order_by('-work_date').first()
        if protocols:
            return protocols.work_date
        return None

    def get_module_id(self, obj) -> int:
        protocols = Protocols.objects.select_related('workplace').filter(product=obj).order_by('-work_date').first()
        if protocols:
            return protocols.workplace.module_id
        return None

    def get_color_code(self, obj) -> str:
        obj = Products.objects.get(id=obj.id)
        if not obj.color_id:
            return None
        return obj.color_id.color_code

    def get_russian_title(self, obj) -> str:
        if not obj.color_id:
            return None
        return obj.color_id.russian_title
