from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.warehouse.models import WarehouseAction
from apps.woffline.models import OfflineWarehouseAction
from apps.woffline.serializers.warehouse_action import (
    OfflineWarehouseActionGetSerializer
)
from apps.warehouse.permissions import WarehousePermission
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline Warehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse_action',
        description='Permission: admin, warehouse, warehouse_writer'
    )
)
class OfflineWarehouseActionListView(ListAPIView):
    queryset = OfflineWarehouseAction.objects.all()
    serializer_class = OfflineWarehouseActionGetSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'type_of_work']

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(WarehouseAction.objects.all())
                serializer = self.serializer_class
                return Response(serializer(query, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.filter_queryset(self.queryset.all())
                return Response(serializer(query, many=True).data)
        except Exception as e:
            global_state.get()
            return Response({'error ': str(e)}, status=400)


@extend_schema(tags=["Offline Warehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse_action',
        description='Permission: admin, warehouse, warehouse_writer'
    )
)
class OfflineWarehouseActionRetrieveView(RetrieveAPIView):
    queryset = OfflineWarehouseAction.objects.all()
    serializer_class = OfflineWarehouseActionGetSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)

    def get(self, request, pk):
        try:
            if global_state.get():
                query = WarehouseAction.objects.filter(pk=pk).first()
                serializer = self.serializer_class
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = self.queryset.first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.get()
            return Response({'error ': str(e)}, status=400)
