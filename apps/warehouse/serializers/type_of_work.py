from rest_framework import serializers

from apps.warehouse.models import TypeOfWork


class TypeOfWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfWork
        fields = "__all__"
