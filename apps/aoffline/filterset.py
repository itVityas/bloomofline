import django_filters as filters

from apps.account.models import User


class UserFilter(filters.FilterSet):
    """
    Filter class for filtering fields
    """
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    username = filters.CharFilter(field_name='username', lookup_expr='iexact')
    cont_username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    start_username = filters.CharFilter(field_name='username', lookup_expr='istartswith')
    end_username = filters.CharFilter(field_name='username', lookup_expr='iendswith')
    fio = filters.CharFilter(field_name='fio', lookup_expr='iexact')
    cont_fio = filters.CharFilter(field_name='fio', lookup_expr='icontains')
    start_fio = filters.CharFilter(field_name='fio', lookup_expr='istartswith')
    end_fio = filters.CharFilter(field_name='fio', lookup_expr='iendswith')
    departmant = filters.CharFilter(field_name='departmant', lookup_expr='iexact')
    cont_departmant = filters.CharFilter(field_name='departmant', lookup_expr='icontains')
    start_departmant = filters.CharFilter(field_name='departmant', lookup_expr='istartswith')
    end_departmant = filters.CharFilter(field_name='departmant', lookup_expr='iendswith')
    position = filters.CharFilter(field_name='position', lookup_expr='iexact')
    cont_position = filters.CharFilter(field_name='position', lookup_expr='icontains')
    start_position = filters.CharFilter(field_name='position', lookup_expr='istartswith')
    end_position = filters.CharFilter(field_name='position', lookup_expr='iendswith')
    room = filters.CharFilter(field_name='room', lookup_expr='iexact')
    cont_room = filters.CharFilter(field_name='room', lookup_expr='icontains')
    start_room = filters.CharFilter(field_name='room', lookup_expr='istartswith')
    end_room = filters.CharFilter(field_name='room', lookup_expr='iendswith')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    created = filters.CharFilter(method='filter_created')
    role = filters.CharFilter(method='filter_role')
    cont_role = filters.CharFilter(method='filter_cont_role')
    start_role = filters.CharFilter(method='filter_start_role')
    end_role = filters.CharFilter(method='filter_end_role')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('username', 'username'),
            ('fio', 'fio'),
            ('departmant', 'departmant'),
            ('position', 'position'),
            ('room', 'room'),
            ('is_active', 'is_active'),
            ('created', 'created'),
            ('role', 'role')
        ),
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'cont_username',
            'start_username',
            'end_username',
            'fio',
            'cont_fio',
            'start_fio',
            'end_fio',
            'departmant',
            'cont_departmant',
            'start_departmant',
            'end_departmant',
            'position',
            'cont_position',
            'start_position',
            'end_position',
            'room',
            'cont_room',
            'start_room',
            'end_room',
            'is_active',
            'created',
            'role',
            'cont_role',
            'start_role',
            'end_role',
        ]

    def filter_created(self, queryset, name, value):
        filter_date = value.split('-')
        if len(filter_date) == 3:
            return queryset.filter(
                created_at__year=filter_date[0],
                created_at__month=filter_date[1],
                created_at__day=filter_date[2])
        return queryset

    def filter_role(self, queryset, name, value):
        return queryset.filter(userroles__role__name=value)

    def filter_cont_role(self, queryset, name, value):
        return queryset.filter(userroles__role__name__icontains=value)

    def filter_start_role(self, queryset, name, value):
        return queryset.filter(userroles__role__name__istartswith=value)

    def filter_end_role(self, queryset, name, value):
        return queryset.filter(userroles__role__name__iendswith=value)
