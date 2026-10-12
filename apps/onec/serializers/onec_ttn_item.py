from rest_framework import serializers

from apps.onec.models import OneCTTNItem
from apps.shtrih.models import Models
from apps.shtrih.serializers.model_name import ModelNamesSerializer


class OneCTTNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTNItem
        fields = "__all__"


class OneCTTNItemListSerializer(serializers.ModelSerializer):
    model_name = ModelNamesSerializer(read_only=True)

    class Meta:
        model = OneCTTNItem
        fields = [
            'model_name',
            'count',
            'available_quantity'
        ]


class OneCTTNItemDesinerSerializer(serializers.ModelSerializer):
    desiner_code = serializers.CharField(write_only=True)
    model_name = ModelNamesSerializer(read_only=True)

    class Meta:
        model = OneCTTNItem
        fields = [
            'model_name',
            'count',
            'desiner_code'
        ]

    def create(self, validated_data):
        desiner_code = validated_data.pop('desiner_code', None)
        model = Models.objects.filter(design_code=desiner_code).first()
        if not model:
            raise serializers.ValidationError("Model with this design code does not exist")
        validated_data['model_name'] = model.name
        return OneCTTNItem.objects.create(**validated_data)
