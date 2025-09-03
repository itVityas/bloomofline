import django_filters as filters

from apps.onec.models import OneCTTN


class OneCTTNFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    number = filters.CharFilter(field_name='number', lookup_expr='iexact')
    start_number = filters.CharFilter(field_name='number', lookup_expr='istartswith')
    end_number = filters.CharFilter(field_name='number', lookup_expr='iendswith')
    cont_number = filters.CharFilter(field_name='number', lookup_expr='icontains')
    series = filters.CharFilter(field_name='series', lookup_expr='iexact')
    start_series = filters.CharFilter(field_name='series', lookup_expr='istartswith')
    end_series = filters.CharFilter(field_name='series', lookup_expr='iendswith')
    cont_series = filters.CharFilter(field_name='series', lookup_expr='icontains')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('number', 'number'),
            ('series', 'series')
        )
    )

    class Meta:
        model = OneCTTN
        fields = (
            'id',
            'number',
            'start_number',
            'end_number',
            'cont_number',
            'series',
            'start_series',
            'end_series',
            'cont_series',
        )
