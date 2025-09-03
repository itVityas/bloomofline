from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.serializers.change_password import (
    ChangePasswordSerializer, ChangeUserPasswordSerializer)
from apps.account.models import User


@extend_schema(tags=['user'])
@extend_schema_view(
    patch=extend_schema(
        summary='Изменение пароля',
        description='isUser',
    ),
)
class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user


@extend_schema(tags=['user'])
@extend_schema_view(
    patch=extend_schema(
        summary='Изменение пароля у пользователя',
        description='isAdmin',
    ),
)
class ChangeUserPasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUserPasswordSerializer
    http_method_names = ['patch']

    def patch(self, request):
        id = request.data.get('id', None)
        user = User.objects.filter(id=id).first()
        serializer = self.get_serializer(user)
        if user:
            user = serializer.update(user, request.data)
            return Response({'success': True})
        return Response({'error': True})
