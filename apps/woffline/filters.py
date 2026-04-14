import django_filters as filters

from apps.woffline.models import (
    OfflineWarehouseTTN,
    OfflineWarehouseDo,
)


class WarehouseTTNFilter(filters.FilterSet):
    number = filters.CharFilter(field_name='ttn_number', lookup_expr='iexact')
    number_start = filters.CharFilter(field_name='ttn_number', lookup_expr='istartswith')
    number_end = filters.CharFilter(field_name='ttn_number', lookup_expr='iendswith')
    number_cont = filters.CharFilter(field_name='ttn_number', lookup_expr='icontains')
    is_close = filters.BooleanFilter(field_name='is_close')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    onec_number = filters.CharFilter(field_name='onec_ttn__number', lookup_expr='iexact')
    onec_series = filters.CharFilter(field_name='onec_ttn__series', lookup_expr='iexact')

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
            'onec_number',
            'onec_series',
        )


class WarehouseDoFilter(filters.FilterSet):
    pk = filters.NumberFilter(field_name='id', lookup_expr='exact')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='exact')
    product = filters.NumberFilter(
        field_name='product', lookup_expr='exact')
    warehouse_ttn = filters.CharFilter(
        field_name='warehouse_ttn__ttn_number', lookup_expr='iexact')
    start_warehouse_ttn = filters.CharFilter(
        field_name='warehouse_ttn__ttn_number', lookup_expr='istartswith')
    cont_warehouse_ttn = filters.CharFilter(
        field_name='warehouse_ttn__ttn_number', lookup_expr='icontains')

    ordering = filters.OrderingFilter(
        fields=(
            ('pk', 'pk'),
            ('update_at', 'update_at'),
            ('create_at', 'create_at'),
            ('quantity', 'quantity'),
            ('product', 'product_id'),
            ('warehouse_ttn', 'warehouse_ttn__ttn_number')
        ),
    )

    class Meta:
        model = OfflineWarehouseDo
        fields = (
            'pk',
            'quantity',
            'create_at',
            'update_at',
            'product',
            'warehouse_ttn',
            'start_warehouse_ttn',
            'cont_warehouse_ttn',
        )
