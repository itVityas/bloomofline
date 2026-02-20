from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.aoffline.models import OfflineUser
from apps.aoffline.exceptions import PasswordException, PasswordEmptyException


class OfflineUserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, write_only=True,
        validators=[UniqueValidator(queryset=OfflineUser.objects.all())])
    password = serializers.CharField(
        required=True, validators=[validate_password], write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = OfflineUser
        fields = [
            'id',
            'username',
            'password',
            'password2',
            'fio',
            'departmant',
            'room',
            'position',
            ]

    def validate(self, attrs):
        password = attrs.get('password', None)
        password2 = attrs.get('password2', None)

        if not password:
            raise PasswordEmptyException
        if password != password2:
            raise PasswordException

        return attrs

    def create(self, validated_data):
        user = OfflineUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            fio=validated_data.get('fio', None),
            departmant=validated_data.get('departmant', None),
            room=validated_data.get('room', None),
            position=validated_data.get('position', None),
        )
        user.save()
        return user
