from rest_framework import serializers

from apps.offwarehouse.models import OfflineTypeOfWork


class OfflineTypeOfWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineTypeOfWork
        fields = "__all__"
