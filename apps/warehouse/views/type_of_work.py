from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.warehouse.models import TypeOfWork
from apps.warehouse.serializers.type_of_work import TypeOfWorkSerializer
from apps.warehouse.permissions import WarehousePermission


@extend_schema(tags=["TypeOfWorkWarehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get list type_of_work warehouse',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    post=extend_schema(
        summary='get list type_of_work warehouse',
        description='Permission: admin, warehouse_writer'
    ),
)
class TypeOfWorkListCreateView(ListCreateAPIView):
    serializer_class = TypeOfWorkSerializer
    queryset = TypeOfWork.objects.all()
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["TypeOfWorkWarehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get type_of_work warehouse',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update type_of_work warehouse',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='update type_of_work warehouse',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete type_of_work warehouse',
        description='Permission: admin, warehouse_writer'
    ),
)
class TypeOfWorkRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TypeOfWorkSerializer
    queryset = TypeOfWork.objects.all()
    permission_classes = [IsAuthenticated, WarehousePermission]
