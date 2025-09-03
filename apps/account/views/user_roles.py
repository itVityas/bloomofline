from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.account.models import UserRoles
from apps.account.serializers.user_roles import UserRolesSerializer
from apps.account.permissions import AccountPermissions


@extend_schema(tags=['UserRoles'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение списка ролей и пользователя',
        description='isUser',
    ),
    post=extend_schema(
        summary='Создание роли и пользователя',
        description='isAdmin',
    ),
)
class UserRolesListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserRolesSerializer
    queryset = UserRoles.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user', 'role')


@extend_schema(tags=['UserRoles'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение роли и пользователя по id',
        description='isUser',
    ),
    put=extend_schema(
        summary='Обновление роли и пользователя',
        description='isAdmin',
    ),
    patch=extend_schema(
        summary='Частичное обновление роли и пользователя',
        description='isAdmin',
    ),
    delete=extend_schema(
        summary='Удаление роли и пользователя',
        description='isAdmin',
    ),
)
class UserRolesDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserRolesSerializer
    queryset = UserRoles.objects.all()
