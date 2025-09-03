from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import Pallet
from apps.warehouse.serializers.pallet import (
    PalletSerializer,
    PalletGenerateSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=["Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='get list pallet',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    post=extend_schema(
        summary='get list pallet',
        description='Permission: admin, warehouse_writer'
    ),
)
class PalletListCreateAPIView(ListCreateAPIView):
    queryset = Pallet.objects.all()
    serializer_class = PalletSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'barcode']
    pagination_class = StandartResultPaginator


@extend_schema(tags=["Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='get pallet',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update pallet',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='update pallet',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete pallet',
        description='Permission: admin, warehouse_writer'
    )
)
class PalletRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Pallet.objects.all()
    serializer_class = PalletSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)


@extend_schema(tags=["Pallet"])
@extend_schema_view(
    post=extend_schema(
        summary='create pallet by ttn_number',
        description='Permission: admin, warehouse_writer'
    )
)
class PalletCreateByTTNAPIView(CreateAPIView):
    queryset = Pallet.objects.all()
    serializer_class = PalletGenerateSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
