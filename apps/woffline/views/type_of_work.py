from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response

from apps.woffline.models import OfflineTypeOfWork
from apps.warehouse.models import TypeOfWork
from apps.woffline.serializers.type_of_work import OfflineTypeOfWorkSerializer
from apps.woffline.permissions import WarehousePermission
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline Warehouse"])
@extend_schema_view(
    get=extend_schema(
        summary='get list type_of_work warehouse',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
)
class OfflineTypeOfWorkListView(ListAPIView):
    serializer_class = OfflineTypeOfWorkSerializer
    queryset = OfflineTypeOfWork.objects.all()
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request):
        try:
            if global_state.get():
                query = TypeOfWork.objects.all()
                serializer = self.serializer_class
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.queryset
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
