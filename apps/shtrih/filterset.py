import django_filters as filter

from .models import Products


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

    class Meta:
        model = Products
        fields = [
            'id',
            'barcode',
            'start_barcode',
            'state',
            'nameplate',
            'quantity',
            'cleared'
        ]
