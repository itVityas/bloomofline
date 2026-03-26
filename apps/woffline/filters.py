import django_filters as filters

from apps.woffline.models import (
    OfflineWarehouseProduct,
    OfflineWarehouseTTN,
    OfflineWarehouseDo,
    OfflineShipment
)


class WarehouseProductFilter(filters.FilterSet):
    is_shipment = filters.BooleanFilter(field_name='is_shipment', lookup_expr='iexact')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='icontains')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('product', 'product_id'),
            ('update_at', 'update_at'),
            ('create_at', 'create_at'),
            ('quantity', 'quantity'),
            ('user', 'user_id'),
        ),
    )

    class Meta:
        model = OfflineWarehouseProduct
        fields = (
            'is_shipment',
            'quantity',
            'create_at',
            'update_at',
        )


class WarehouseTTNFilter(filters.FilterSet):
    number = filters.CharFilter(field_name='ttn_number', lookup_expr='iexact')
    number_start = filters.CharFilter(field_name='ttn_number', lookup_expr='istartswith')
    number_end = filters.CharFilter(field_name='ttn_number', lookup_expr='iendswith')
    number_cont = filters.CharFilter(field_name='ttn_number', lookup_expr='icontains')
    is_close = filters.BooleanFilter(field_name='is_close')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('ttn_number', 'ttn_number'),
            ('is_close', 'is_close'),
            ('date', 'date'),
            ('warehouse', 'warehouse_id'),
            ('warehouse_action', 'warehouse_action_id'),
            ('user', 'user_id'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
    )

    class Meta:
        model = OfflineWarehouseTTN
        fields = (
            'number',
            'number_start',
            'number_end',
            'number_cont',
            'is_close',
            'date',
        )


class WarehouseDoFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='icontains')
    warehouse_product = filters.NumberFilter(
        field_name='warehouse_product', lookup_expr='exact')
    warehouse_ttn = filters.NumberFilter(
        field_name='warehouse_ttn', lookup_expr='exact')
    user = filters.NumberFilter(field_name='user', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('update_at', 'update_at'),
            ('create_at', 'create_at'),
            ('quantity', 'quantity'),
            ('user', 'user_id'),
            ('warehouse_product', 'warehouse_product_id'),
            ('warehouse_ttn', 'warehouse_ttn_id')
        ),
    )

    class Meta:
        model = OfflineWarehouseDo
        fields = (
            'id',
            'quantity',
            'create_at',
            'update_at',
            'user',
            'warehouse_product',
            'warehouse_ttn',
        )


class ShipmentFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='icontains')
    warehouse_product = filters.NumberFilter(
        field_name='warehouse_product', lookup_expr='exact')
    warehouse_ttn = filters.NumberFilter(
        field_name='warehouse_ttn', lookup_expr='exact')
    user = filters.NumberFilter(field_name='user', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('update_at', 'update_at'),
            ('create_at', 'create_at'),
            ('quantity', 'quantity'),
            ('user', 'user_id'),
            ('warehouse_product', 'warehouse_product_id'),
            ('warehouse_ttn', 'warehouse_ttn_id')
        ),
    )

    class Meta:
        model = OfflineShipment
        fields = (
            'id',
            'quantity',
            'create_at',
            'update_at',
            'user',
            'warehouse_product',
            'warehouse_ttn',
        )
