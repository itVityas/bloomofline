from rest_framework.generics import (
    ListAPIView, DestroyAPIView, UpdateAPIView,
    RetrieveAPIView, GenericAPIView)
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from apps.account.models import User, UserRoles
from apps.account.serializers.user import UserSerializer, UserUpdateSerializer
from apps.account.permissions import AccountPermissions
from Bloom.paginator import StandartResultPaginator
from apps.account.filterset import UserFilter


@extend_schema(tags=['user'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение списка всех пользователй',
        description='isUser',
    ),
)
class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter


@extend_schema(tags=['user'])
@extend_schema_view(
    put=extend_schema(
        summary='Обновление пользователя',
        description='isAdmin',
    ),
    patch=extend_schema(
        summary='Частичное обновление пользователя',
        description='isAdmin',
    ),
    delete=extend_schema(
        summary='Удаление пользователя',
        description='isAdmin',
    ),
)
class UserDetailedView(DestroyAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


@extend_schema(tags=['user'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение пользователя по id',
        description='isUser',
    )
)
class UserRetrieveView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(tags=['user'])
@extend_schema_view(
    delete=extend_schema(
        summary='Удаление роли у пользователя',
        description='isAdmin',
        parameters=[
            OpenApiParameter(
                name='user',
                location=OpenApiParameter.QUERY,
                description='User id',
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name='role',
                location=OpenApiParameter.QUERY,
                description='Role id',
                required=True,
                type=int,
            ),
        ]
    ),
)
class UserRoleDeleteView(GenericAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def delete(self, request):
        id_role = request.query_params.get('role', None)
        id_user = request.query_params.get('user', None)
        if not id_role or not id_user:
            print(id_role, id_user)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        UserRoles.objects.filter(
            user_id=id_user, role_id=id_role
        ).delete()
        return Response(
            UserSerializer(User.objects.get(id=id_user)).data,
            status=status.HTTP_200_OK)
