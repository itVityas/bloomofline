from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.account.exceptions import (
    PasswordEmptyException, OldPasswordException, PasswordException)
from apps.account.models import User


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True, validators=[validate_password], write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    old_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2', 'old_password']

    def validate(self, attrs):
        password = attrs.get('password', None)
        password2 = attrs.get('password2', None)

        if not password:
            raise PasswordEmptyException
        if password != password2:
            raise PasswordException
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise OldPasswordException
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ChangeUserPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    password = serializers.CharField(
        required=True, validators=[validate_password], write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'password2']

    def update(self, instance, attrs):
        password = attrs.get('password', None)
        password2 = attrs.get('password2', None)

        if not password:
            raise PasswordEmptyException
        if password != password2:
            raise PasswordException
        instance.set_password(password)
        instance.save()
        return instance
