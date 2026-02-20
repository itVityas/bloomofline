from rest_framework import serializers

from apps.aoffline.models import OfflineUserRoles


class OfflineUserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineUserRoles
        fields = '__all__'
