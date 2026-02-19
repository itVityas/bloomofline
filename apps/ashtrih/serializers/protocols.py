from rest_framework import serializers

from apps.ashtrih.models import Protocols
from apps.ashtrih.serializers.products import ProductGetSerializer
from apps.ashtrih.serializers.workplaces import WorkplacesSerializer


class ProtocolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocols
        fields = "__all__"


class ProtocolsFullSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(read_only=True, many=False)
    workplace = WorkplacesSerializer(read_only=True, many=False)

    class Meta:
        model = Protocols
        fields = "__all__"
