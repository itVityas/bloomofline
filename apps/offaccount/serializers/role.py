from rest_framework import serializers

from apps.offaccount.models import OfflineRole


class OfflineRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineRole
        fields = '__all__'
