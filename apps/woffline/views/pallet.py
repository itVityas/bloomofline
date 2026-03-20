from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.warehouse.models import Pallet
from apps.woffline.models import OfflinePallet
from apps.woffline.serializers.pallet import (
    OfflinePalletSerializer,
    OfflinePalletGenerateSerializer
)
from apps.warehouse.serializers.pallet import (
    PalletSerializer,
    PalletGenerateSerializer
)
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='get list pallet',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    post=extend_schema(
        summary='get list pallet',
        description='Permission: admin, warehouse_writer'
    ),
)
class OfflinePalletListCreateAPIView(ListCreateAPIView):
    queryset = OfflinePallet.objects.all()
    serializer_class = OfflinePalletSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'barcode']
    pagination_class = StandartResultPaginator

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(Pallet.objects.all())
                serializer = self.serializer_class
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.filter_queryset(self.queryset)
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)

    def post(self, request):
        try:
            if global_state.get():
                serializer = PalletSerializer(data=request.data)
                if serializer.is_valid():
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='get pallet',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update pallet',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='update pallet',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete pallet',
        description='Permission: admin, warehouse_writer'
    )
)
class OfflinePalletRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = OfflinePallet.objects.all()
    serializer_class = OfflinePalletSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)

    def get(self, request, pk):
        try:
            if global_state.get():
                query = Pallet.objects.filter(pk=pk).first()
                serializer = self.serializer_class
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

    def put(self, request, pk):
        try:
            if global_state.get():
                query = Pallet.objects.filter(pk=pk).first()
                serializer = self.serializer_class(query, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                query = self.queryset.filter(pk=pk).first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                serializer = self.serializer_class(query, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)

    def patch(self, request, pk):
        try:
            if global_state.get():
                query = Pallet.objects.filter(pk=pk).first()
                serializer = self.serializer_class(query, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                query = self.queryset.filter(pk=pk).first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                serializer = self.serializer_class(query, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.get()
            return Response({'error': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            if global_state.get():
                query = Pallet.objects.filter(pk=pk).first()
                if query:
                    query.delete()
                    return Response({'message': 'deleted'}, status=200)
                return Response({'error': 'not found'}, status=404)
            else:
                query = self.queryset.filter(pk=pk).first()
                if query:
                    query.delete()
                    return Response({'message': 'deleted'}, status=200)
                return Response({'error': 'not found'}, status=404)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline Pallet"])
@extend_schema_view(
    post=extend_schema(
        summary='create pallet by ttn_number',
        description='Permission: admin, warehouse_writer'
    )
)
class OfflinePalletCreateByTTNAPIView(CreateAPIView):
    queryset = OfflinePallet.objects.all()
    serializer_class = OfflinePalletGenerateSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)

    def post(self, request):
        try:
            if global_state.get():
                serializer = PalletGenerateSerializer(data=request.data)
                if serializer.is_valid():
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
