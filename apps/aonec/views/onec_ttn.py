from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.aonec.models import OfflineOneCTTN
from apps.aonec.serializers.onec_ttn import (
    OfflineOneCTTNGetSerializer,
    OfflineOneCTTNPostSerializer,
    OfflineOneCTTNFullSerializer
)
from apps.aonec.permissions import Warehouse1CPermission
from apps.aonec.filters import OneCTTNFilter


@extend_schema(tags=['Offline OfflineOneCTTN'])
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


@extend_schema(tags=["Offline OfflineOneCTTN"])
@extend_schema_view(
    post=extend_schema(
        summary='Create OneC TTN',
        description='Permission: admin, warehouse_writer'
        ),
)
class OfflineOneCTTNCreateAPIView(CreateAPIView):
    queryset = OfflineOneCTTN.objects.all()
    serializer_class = OfflineOneCTTNPostSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['Offline OfflineOneCTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTN',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
    put=extend_schema(
        summary='Update OneC TTN',
        description='Permission: admin, warehouse_writer'
        ),
    patch=extend_schema(
        summary='Update OneC TTN',
        description='Permission: admin, warehouse_writer'
        ),
    delete=extend_schema(
        summary='Delete OneC TTN',
        description='Permission: admin, warehouse_writer'
        ),
)
class OfflineOneCTTNRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OfflineOneCTTN.objects.all()
    serializer_class = OfflineOneCTTNPostSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['Offline OfflineOneCTTN'])
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


@extend_schema(tags=['Offline OfflineOneCTTN'])
@extend_schema_view(
    post=extend_schema(
        summary='create OneC TTN and list OfflineOneCTTNitems',
        description='Permission: admin, warehouse_writer'
        ),
)
class OfflineOneCTTNFullCreateAPIView(CreateAPIView):
    queryset = OfflineOneCTTN.objects.all()
    serializer_class = OfflineOneCTTNFullSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]
