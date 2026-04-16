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
from apps.onec.serializers.onec_ttn import (
    OneCTTNGetSerializer,
)
from apps.aonec.permissions import Warehouse1CPermission
from apps.aonec.filters import OneCTTNFilter
from apps.onec.filters import OneCTTNFilter as OnlineOneCTTNFilter
from bloomofline.global_state import global_state


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

    def get_filterset_class(self):
        if global_state.get():
            return OnlineOneCTTNFilter
        else:
            return OneCTTNFilter

    def filter_queryset(self, queryset):
        filterset_class = self.get_filterset_class()

        if filterset_class:
            filterset = filterset_class(
                self.request.GET,
                queryset=queryset,
                request=self.request
            )
            if filterset.is_valid():
                return filterset.qs
            else:
                return queryset.none()

        return queryset

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(OneCTTN.objects.all())
                serializer = OneCTTNGetSerializer
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.filter_queryset(self.queryset)
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
        except Exception as e:
            global_state.set()
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

    def get(self, request, pk):
        try:
            if global_state.get():
                query = OneCTTN.objects.filter(pk=pk).first()
                serializer = OneCTTNGetSerializer
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = self.queryset.filter(pk=pk).first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
