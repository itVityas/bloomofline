from rest_framework import serializers

from apps.aoffline.models import OfflineUser, OfflineRole
from apps.aoffline.serializers.role import OfflineRoleSerializer


class OfflineUserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = OfflineUser
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
        roles = OfflineRole.objects.filter(offlineuserroles__user=obj)
        role_serializer = OfflineRoleSerializer(roles, many=True)
        return role_serializer.data


class OfflineUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineUser
        fields = [
                'username',
                'fio',
                'is_active',
                'departmant',
                'room',
                'position',
            ]
