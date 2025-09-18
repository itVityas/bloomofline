from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from apps.account.exceptions import EmptyUserException
from apps.account.serializers.user import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        username = attrs.get('username', None)

        if not username:
            raise EmptyUserException
        user = get_user_model().objects.filter(username=username).first()
        if user:
            user.last_login = timezone.now()
            user.save()
        data['user'] = UserSerializer(user).data
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
