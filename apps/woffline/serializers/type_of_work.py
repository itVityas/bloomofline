from rest_framework import serializers

from apps.woffline.models import OfflineTypeOfWork


class OfflineTypeOfWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineTypeOfWork
        fields = "__all__"
