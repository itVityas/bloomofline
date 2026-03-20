from rest_framework.generics import (ListAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.warehouse.models import Warehouse
from apps.woffline.models import OfflineWarehouse
from apps.woffline.serializers.warehouse import OfflineWarehouseSerializer
from apps.woffline.permissions import WarehousePermission
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline Warehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
)
class OfflineWarehouseListView(ListAPIView):
    queryset = OfflineWarehouse.objects.all()
    serializer_class = OfflineWarehouseSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'is_active', 'date']

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(Warehouse.objects.all())
                serializer = self.serializer_class
                return Response(serializer(query, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.filter_queryset(self.queryset.all())
                return Response(serializer(query, many=True).data)
        except Exception as e:
            global_state.set()
            return Response({'error ': str(e)}, status=400)
