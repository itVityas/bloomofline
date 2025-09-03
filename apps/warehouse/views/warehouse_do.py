from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import WarehouseDo
from apps.warehouse.serializers.warehouse_do import (
    WarehouseDoGetSerializer,
    WarehouseDoPostSerializer,
    WarehouseDoPalletSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import WarehouseDoFilter


@extend_schema(tags=["WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse do',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class WarehouseDoListAPIView(ListAPIView):
    queryset = WarehouseDo.objects.all()
    serializer_class = WarehouseDoGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseDoFilter


@extend_schema(tags=["WarehouseDo"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new WarehouseDo',
        description='Permission: admin, warehouse_writer',
    )
)
class WarehouseDoCreateAPIView(CreateAPIView):
    queryset = WarehouseDo.objects.all()
    serializer_class = WarehouseDoPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseDo',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    patch=extend_schema(
        summary='Update a WarehouseDo',
        description='Permission: admin warehouse_writer',
    ),
    put=extend_schema(
        summary='Update a WarehouseDo',
        description='Permission: admin warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete a WarehouseDo',
        description='Permission: admin warehouse_writer',
    ),
)
class WarehouseDoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WarehouseDo.objects.all()
    serializer_class = WarehouseDoPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseDo',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class WarehouseDoRetrieveAPIView(RetrieveAPIView):
    queryset = WarehouseDo.objects.all()
    serializer_class = WarehouseDoGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["WarehouseDo"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a WarehouseDo by barcode in pallet',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class WarehouseDoBarcodePalletAPIView(CreateAPIView):
    queryset = WarehouseDo.objects.all()
    serializer_class = WarehouseDoPalletSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
