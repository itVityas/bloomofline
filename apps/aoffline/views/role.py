from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.account.models import Role
from apps.account.serializers.role import RoleSerializer
from apps.account.permissions import AccountPermissions


@extend_schema(tags=['Role'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение списка ролей',
        description='isUser',
    ),
    post=extend_schema(
        summary='Создание роли',
        description='isAdmin',
    ),
)
class RoleListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


@extend_schema(tags=['Role'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение роли по id',
        description='isUser',
    ),
    put=extend_schema(
        summary='Обновление роли',
        description='isAdmin',
    ),
    patch=extend_schema(
        summary='Частичное обновление роли',
        description='isAdmin',
    ),
    delete=extend_schema(
        summary='Удаление роли',
        description='isAdmin',
    ),
)
class RoleDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
