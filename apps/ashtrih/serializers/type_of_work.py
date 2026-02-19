from rest_framework import serializers

from apps.ashtrih.models import TypesOfWork


class TypesOfWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypesOfWork
        fields = "__all__"
