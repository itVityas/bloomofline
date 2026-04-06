from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.warehouse.models import Pallet
from apps.woffline.models import OfflinePallet
from apps.woffline.serializers.pallet import (
    OfflinePalletSerializer,
    OfflinePalletGenerateSerializer,
    OfflinePalletProductsSerializer,
    OfflinePalletDecomposeSerializer,
)
from apps.warehouse.serializers.pallet import (
    PalletSerializer,
    PalletGenerateSerializer,
    PalletProductsSerializer,
)
from apps.shtrih.models import Models
from apps.ashtrih.models import OfflineModels
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='get list pallet',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
)
class OfflinePalletListCreateAPIView(ListAPIView):
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
                serializer = PalletSerializer
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
                serializer = PalletSerializer
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
                serializer = PalletSerializer(query, data=request.data)
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
                serializer = PalletSerializer(query, data=request.data, partial=True)
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
            global_state.set()
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
        summary='create pallet by ttn_number or return existing',
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
                    warehouse_ttn = serializer.save()
                    return Response(PalletSerializer(warehouse_ttn).data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    warehouse_ttn = serializer.save()
                    return Response(OfflinePalletSerializer(warehouse_ttn).data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='get pallet with products',
        description='Permission: admin, warehouse, warehouse_writer',
        parameters=[
            OpenApiParameter(name='ttn_number', description='ttn_number', required=True, type=str),
        ]
    ),
)
class OfflinePalletWithProductsListAPIView(ListAPIView):
    queryset = OfflinePallet.objects.all()
    serializer_class = OfflinePalletProductsSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = None

    def get(self, request):
        try:
            ttn_number = request.query_params.get('ttn_number', None)
            if global_state.get():
                query = Pallet.objects.filter(ttn_number__ttn_number=ttn_number).first()
                if not query:
                    return Response({'error': 'Палет не найден'}, status=404)
                serializer = PalletProductsSerializer
                return Response(serializer(query, many=False).data)
            else:
                query = OfflinePallet.objects.filter(ttn_number__ttn_number=ttn_number).first()
                if not query:
                    return Response({'error': 'Палет не найден'}, status=404)
                serializer = self.serializer_class
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline Pallet"])
@extend_schema_view(
    get=extend_schema(
        summary='decompose pallet barcode',
        description='''Permission: admin, warehouse_writer
        barcode 20 symbols:
        model: 5 (model.code),
        month: 2,
        year: 2,
        quantity: 3,
        ttn_number: 8''',
        parameters=[
            OpenApiParameter(name='barcode', description='pallet barcode', required=True, type=str),
        ]
    )
)
class OfflinePalletDecomposeAPIView(APIView):
    query = Pallet.objects.all()
    serializer_class = OfflinePalletDecomposeSerializer
    permission_classes = (IsAuthenticated, WarehousePermission)

    def get(self, request):
        barcode = request.query_params.get('barcode', None)
        if not barcode or len(barcode) != 20:
            return Response({'error': 'invalid barcode'}, status=400)
        model_code = barcode[0:5]
        month = barcode[5:7]
        year = barcode[7:9]
        quantity = barcode[9:12]
        ttn_number = barcode[12:20]

        try:
            if global_state.get():
                model = Models.objects.filter(code=model_code).first()
                if not model:
                    return Response({'error': 'model not found'}, status=404)
                return Response({
                    'model_name': model.name.name,
                    'month': month,
                    'year': year,
                    'quantity': quantity,
                    'ttn_number': ttn_number,
                }, status=200)
            else:
                model = OfflineModels.objects.filter(code=model_code).first()
                if not model:
                    return Response({'error': 'model not found'}, status=404)
                return Response({
                    'model_name': model.name.name,
                    'month': month,
                    'year': year,
                    'quantity': quantity,
                    'ttn_number': ttn_number,
                }, status=200)
        except Exception as e:
            global_state.set()
            return Response({'error ': str(e)}, status=400)
