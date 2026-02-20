from rest_framework import serializers

from apps.aoffline.models import OfflineRole


class OfflineRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineRole
        fields = '__all__'
