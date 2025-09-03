from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.onec.models import OneCTTNItem
from apps.onec.serializers.onec_ttn_item import OneCTTNItemSerializer
from apps.onec.permissions import Warehouse1CPermission


@extend_schema(tags=['OneCTTNItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTN item',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
    put=extend_schema(
        summary='Update OneC TTN item',
        description='Permission: admin, warehouse_writer'
        ),
    patch=extend_schema(
        summary='Update OneC TTN item',
        description='Permission: admin, warehouse_writer'
        ),
    delete=extend_schema(
        summary='Delete OneC TTN item',
        description='Permission: admin, warehouse_writer'
        ),
    )
class OneCTTNItemRUDView(RetrieveUpdateDestroyAPIView):
    queryset = OneCTTNItem.objects.all()
    serializer_class = OneCTTNItemSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['OneCTTNItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTN items',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
    post=extend_schema(
        summary='Create OneC TTN items',
        description='Permission: admin, warehouse_writer'
        ),
    )
class OneCTTNItemCreateListView(ListCreateAPIView):
    queryset = OneCTTNItem.objects.all()
    serializer_class = OneCTTNItemSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]
