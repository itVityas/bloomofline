from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.account.models import User
from apps.account.serializers.register import UserRegisterSerializer
from apps.account.permissions import AccountPermissions


@extend_schema(tags=['user'])
@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        description='isAdmin',
    ),
)
class RegistrationView(CreateAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
