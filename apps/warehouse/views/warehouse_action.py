from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import WarehouseAction
from apps.warehouse.serializers.warehouse_action import (
    WarehouseActionGetSerializer,
    WarehouseActionPostSerializer
)
from apps.warehouse.permissions import WarehousePermission


@extend_schema(tags=["WarehouseAction"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse_action',
        description='Permission: admin, warehouse, warehouse_writer'
    )
)
class WarehouseActionListView(ListAPIView):
    queryset = WarehouseAction.objects.all()
    serializer_class = WarehouseActionGetSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'type_of_work']


@extend_schema(tags=["WarehouseAction"])
@extend_schema_view(
    post=extend_schema(
        summary='create warehouse_action',
        description='Permission: admin, warehouse_writer'
    )
)
class WarehouseActionCreateView(CreateAPIView):
    queryset = WarehouseAction.objects.all()
    serializer_class = WarehouseActionPostSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)


@extend_schema(tags=["WarehouseAction"])
@extend_schema_view(
    get=extend_schema(
        summary='get update delete warehouse_action',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update warehouse_action',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete warehouse_action',
        description='Permission: admin, warehouse_writer'
    ),
)
class WarehouseActionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = WarehouseAction.objects.all()
    serializer_class = WarehouseActionPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["WarehouseAction"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse_action',
        description='Permission: admin, warehouse, warehouse_writer'
    )
)
class WarehouseActionRetrieveView(RetrieveAPIView):
    queryset = WarehouseAction.objects.all()
    serializer_class = WarehouseActionGetSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
