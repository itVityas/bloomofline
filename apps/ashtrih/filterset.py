import django_filters as filter

from .models import Products, ModelNames, Models


class ProductFilter(filter.FilterSet):
    """
    FilterSet for querying Products with various filtering options.
    Provides precise and flexible filtering capabilities for product inventory.

    Attributes:
        start_barcode: Filter products by barcode prefix (case-insensitive)
    """
    start_barcode = filter.CharFilter(
        field_name='barcode',
        lookup_expr='istartswith',
        help_text="Filter products by barcode prefix (case insensitive)",)
    omega_model_id = filter.CharFilter(
        field_name='model__omega_model_id',
        lookup_expr='exact',
        help_text="Filter products by omega model ID (case insensitive)",)
    omega_variant_id = filter.CharFilter(
        field_name='model__omega_variant_id',
        lookup_expr='exact',
        help_text="Filter products by omega variant ID (case insensitive)",)
    state = filter.NumberFilter(
        field_name='state',
        lookup_expr='exact',
        help_text="Filter products by state (case insensitive)",)

    class Meta:
        model = Products
        fields = [
            'id',
            'barcode',
            'start_barcode',
            'state',
            'nameplate',
            'quantity',
            'cleared',
            'omega_model_id',
            'omega_variant_id',
            'state',
        ]


class ModelNamesFilter(filter.FilterSet):
    """
    FilterSet for querying ModelNames with various filtering options.
    Provides precise and flexible filtering capabilities for model names.

    Attributes:
        name: Filter model names by name (case-insensitive)
    """
    name = filter.CharFilter(
        field_name='name',
        lookup_expr='iexact',
        help_text="Filter model names by name (case insensitive)",)
    start_name = filter.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
        help_text="Filter model names by name prefix (case insensitive)",)
    end_name = filter.CharFilter(
        field_name='name',
        lookup_expr='iendswith',
        help_text="Filter model names by name suffix (case insensitive)",)
    cont_name = filter.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text="Filter model names by name containing (case insensitive)",)
    short_name = filter.CharFilter(
        field_name='short_name',
        lookup_expr='iexact',
        help_text="Filter model names by short name (case insensitive)",)
    start_short_name = filter.CharFilter(
        field_name='short_name',
        lookup_expr='istartswith',
        help_text="Filter model names by short name prefix (case insensitive)",)
    end_short_name = filter.CharFilter(
        field_name='short_name',
        lookup_expr='iendswith',
        help_text="Filter model names by short name suffix (case insensitive)",)
    cont_short_name = filter.CharFilter(
        field_name='short_name',
        lookup_expr='icontains',
        help_text="Filter model names by short name containing (case insensitive)",)

    class Meta:
        model = ModelNames
        fields = [
            'id',
            'name',
            'start_name',
            'end_name',
            'cont_name',
            'short_name',
            'start_short_name',
            'end_short_name',
            'cont_short_name'
        ]


class ModelFilter(filter.FilterSet):
    pk = filter.NumberFilter(
        field_name='id',
        lookup_expr='exact',
        help_text="Filter models by ID",)
    production_code = filter.NumberFilter(
        field_name='production_code',
        lookup_expr='exact',
        help_text="Filter models by production code",)
    variant_code = filter.CharFilter(
        field_name='variant_code',
        lookup_expr='iexact',
        help_text="Filter models by variant code (case insensitive)",)
    code = filter.NumberFilter(
        field_name='code',
        lookup_expr='exact',
        help_text="Filter models by code",)
    name = filter.CharFilter(
        field_name='name__name',
        lookup_expr='iexact',
        help_text="Filter models by name (case insensitive)",)
    start_name = filter.CharFilter(
        field_name='name__name',
        lookup_expr='istartswith',
        help_text="Filter models by name prefix (case insensitive)",)
    end_name = filter.CharFilter(
        field_name='name__name',
        lookup_expr='iendswith',
        help_text="Filter models by name suffix (case insensitive)",)
    cont_name = filter.CharFilter(
        field_name='name__name',
        lookup_expr='icontains',
        help_text="Filter models by name containing (case insensitive)",)
    short_name = filter.CharFilter(
        field_name='name__short_name',
        lookup_expr='iexact',
        help_text="Filter models by short name (case insensitive)",)
    start_short_name = filter.CharFilter(
        field_name='name__short_name',
        lookup_expr='istartswith',
        help_text="Filter models by short name prefix (case insensitive)",)
    end_short_name = filter.CharFilter(
        field_name='name__short_name',
        lookup_expr='iendswith',
        help_text="Filter models by short name suffix (case insensitive)",)
    cont_short_name = filter.CharFilter(
        field_name='name__short_name',
        lookup_expr='icontains',
        help_text="Filter models by short name containing (case insensitive)",)

    class Meta:
        model = Models
        fields = [
            'pk',
            'production_code',
            'variant_code',
            'code',
            'name',
            'cont_name',
            'start_name',
            'end_name',
            'short_name',
            'start_short_name',
            'end_short_name',
            'cont_short_name',
        ]
