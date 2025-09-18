from rest_framework import serializers

from apps.account.models import UserRoles


class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'
