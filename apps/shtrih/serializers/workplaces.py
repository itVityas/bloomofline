from rest_framework import serializers

from apps.shtrih.models import Workplaces
from apps.shtrih.serializers.type_of_work import TypesOfWorkSerializer
from apps.shtrih.serializers.module import ModulesSerializer


class WorkplacesSerializer(serializers.ModelSerializer):
    type_of_work = TypesOfWorkSerializer(many=False, read_only=True)
    module = ModulesSerializer(many=False, read_only=True)

    class Meta:
        model = Workplaces
        fields = "__all__"
