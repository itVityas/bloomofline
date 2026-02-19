from rest_framework import serializers

from apps.ashtrih.models import Workplaces
from apps.ashtrih.serializers.type_of_work import TypesOfWorkSerializer
from apps.ashtrih.serializers.module import ModulesSerializer


class WorkplacesSerializer(serializers.ModelSerializer):
    type_of_work = TypesOfWorkSerializer(many=False, read_only=True)
    module = ModulesSerializer(many=False, read_only=True)

    class Meta:
        model = Workplaces
        fields = "__all__"
