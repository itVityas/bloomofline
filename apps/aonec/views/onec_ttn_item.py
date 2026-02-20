from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.aonec.models import OfflineOneCTTNItem
from apps.aonec.serializers.onec_ttn_item import OfflineOneCTTNItemSerializer
from apps.aonec.permissions import Warehouse1CPermission


@extend_schema(tags=['Offline OneCTTNItem'])
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
class OfflineOneCTTNItemRUDView(RetrieveUpdateDestroyAPIView):
    queryset = OfflineOneCTTNItem.objects.all()
    serializer_class = OfflineOneCTTNItemSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['Offline OneCTTNItem'])
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
class OfflineOneCTTNItemCreateListView(ListCreateAPIView):
    queryset = OfflineOneCTTNItem.objects.all()
    serializer_class = OfflineOneCTTNItemSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]
