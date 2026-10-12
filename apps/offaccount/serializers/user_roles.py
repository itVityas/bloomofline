from rest_framework import serializers

from apps.offaccount.models import OfflineUserRoles


class OfflineUserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineUserRoles
        fields = '__all__'
