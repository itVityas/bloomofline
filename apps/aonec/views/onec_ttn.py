from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.aonec.models import OfflineOneCTTN
from apps.onec.models import OneCTTN
from apps.aonec.serializers.onec_ttn import (
    OfflineOneCTTNGetSerializer,
)
from apps.aonec.permissions import Warehouse1CPermission
from apps.aonec.filters import OneCTTNFilter
from bloomofline.db_routers import ModelDatabaseRouter


@extend_schema(tags=['Offline OneCTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTNs',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
)
class OfflineOneCTTNListAPIView(ListAPIView):
    queryset = OfflineOneCTTN.objects.all()
    serializer_class = OfflineOneCTTNGetSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OneCTTNFilter

    def get(self, request):
        try:
            if ModelDatabaseRouter().check_mssql_connection():
                query = OneCTTN.objects.all()
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


@extend_schema(tags=['Offline OneCTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTN',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
)
class OfflineOneCTTNRetrieveAPIView(RetrieveAPIView):
    queryset = OfflineOneCTTN.objects.all()
    serializer_class = OfflineOneCTTNGetSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]

    def get(self, request):
        try:
            if ModelDatabaseRouter().check_mssql_connection():
                query = OneCTTN.objects.all()
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
