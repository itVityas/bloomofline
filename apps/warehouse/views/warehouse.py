from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import Warehouse
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.permissions import WarehousePermission


@extend_schema(tags=["Warehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    post=extend_schema(
        summary='get list warehouse',
        description='Permission: admin, warehouse_writer'
    ),
)
class WarehouseListCreateView(ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'is_active', 'date']


@extend_schema(tags=["Warehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update warehouse',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='update warehouse',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete warehouse',
        description='Permission: admin, warehouse_writer'
    ),
)
class WarehouseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
