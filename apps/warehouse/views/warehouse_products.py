from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers.warehouse_products import (
    WarehouseProductGetSerializer,
    WarehouseProductPostSerializer,
    WarehouseProductBarcodeSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import WarehouseProductFilter


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse products',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class WarehouseProductListAPIView(ListAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseProductFilter


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse product',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class WarehouseProductRetrieveAPIView(RetrieveAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    post=extend_schema(
        summary='create warehouse product',
        description='Permission: admin, warehouse_writer'
    )
)
class WarehouseProductCreateAPIView(CreateAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    post=extend_schema(
        summary='create warehouse product by barcode',
        description='Permission: admin, warehouse_writer'
    )
)
class WarehouseProductCreateByBarcodeAPIView(CreateAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductBarcodeSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            WarehouseProductGetSerializer(instance).data,
            status=status.HTTP_201_CREATED)


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse product',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update warehouse product',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='partial update warehouse product',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete warehouse product',
        description='Permission: admin, warehouse_writer'
    )
)
class WarehouseProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
