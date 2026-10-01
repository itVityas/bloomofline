from rest_framework import serializers

from apps.shtrih.models import ShtrihUser


class ShtrihUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShtrihUser
        fields = '__all__'
