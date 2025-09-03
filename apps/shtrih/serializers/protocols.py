from rest_framework import serializers

from apps.shtrih.models import Protocols
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.shtrih.serializers.workplaces import WorkplacesSerializer


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
