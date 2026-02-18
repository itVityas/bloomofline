from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.aonec.models import OneCTTN
from apps.aonec.serializers.onec_ttn import (
    OneCTTNGetSerializer,
    OneCTTNPostSerializer,
    OneCTTNFullSerializer
)
from apps.aonec.permissions import Warehouse1CPermission
from apps.aonec.filters import OneCTTNFilter


@extend_schema(tags=['OneCTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTNs',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
)
class OneCTTNListAPIView(ListAPIView):
    queryset = OneCTTN.objects.all()
    serializer_class = OneCTTNGetSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OneCTTNFilter


@extend_schema(tags=["OneCTTN"])
@extend_schema_view(
    post=extend_schema(
        summary='Create OneC TTN',
        description='Permission: admin, warehouse_writer'
        ),
)
class OneCTTNCreateAPIView(CreateAPIView):
    queryset = OneCTTN.objects.all()
    serializer_class = OneCTTNPostSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['OneCTTN'])
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
class OneCTTNRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OneCTTN.objects.all()
    serializer_class = OneCTTNPostSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['OneCTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC TTN',
        description='Permission: admin, warehouse, warehouse_writer'
        ),
)
class OneCTTNRetrieveAPIView(RetrieveAPIView):
    queryset = OneCTTN.objects.all()
    serializer_class = OneCTTNGetSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]


@extend_schema(tags=['OneCTTN'])
@extend_schema_view(
    post=extend_schema(
        summary='create OneC TTN and list onecttnitems',
        description='Permission: admin, warehouse_writer'
        ),
)
class OneCTTNFullCreateAPIView(CreateAPIView):
    queryset = OneCTTN.objects.all()
    serializer_class = OneCTTNFullSerializer
    permission_classes = [IsAuthenticated, Warehouse1CPermission]
