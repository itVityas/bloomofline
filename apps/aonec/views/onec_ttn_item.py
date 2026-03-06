from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response

from apps.aonec.models import OfflineOneCTTNItem
from apps.onec.models import OneCTTNItem
from apps.aonec.serializers.onec_ttn_item import OfflineOneCTTNItemSerializer
from apps.aonec.permissions import Warehouse1CPermission
from bloomofline.db_routers import ModelDatabaseRouter


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
class OfflineOneCTTNItemListView(ListAPIView):
    queryset = OfflineOneCTTNItem.objects.all()
    serializer_class = OfflineOneCTTNItemSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]

    def get(self, request):
        try:
            if ModelDatabaseRouter().check_mssql_connection():
                query = OneCTTNItem.objects.all()
                serializer = self.serializer_class
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.queryset
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
        except Exception as e:
            return Response({'error': str(e)})
