from rest_framework import serializers

from apps.account.models import User, Role
from apps.account.serializers.role import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'fio',
            'is_active',
            'departmant',
            'room',
            'position',
            'created_at',
            'updated_at',
            'roles',
            ]

    def get_roles(self, obj) -> dict:
        roles = Role.objects.filter(userroles__user=obj)
        role_serializer = RoleSerializer(roles, many=True)
        return role_serializer.data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'fio',
            'is_active',
            'departmant',
            'room',
            'position',
            ]
