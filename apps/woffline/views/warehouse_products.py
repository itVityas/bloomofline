from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.warehouse.models import WarehouseProduct
from apps.woffline.models import OfflineWarehouseProduct
from apps.warehouse.serializers.warehouse_products import (
    WarehouseProductGetSerializer,
    WarehouseProductPostSerializer,
    WarehouseProductBarcodeSerializer
)
from apps.woffline.serializers.warehouse_products import (
    OfflineWarehouseProductGetSerializer,
    OfflineWarehouseProductPostSerializer,
    OfflineWarehouseProductBarcodeSerializer,
)
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from apps.woffline.filters import WarehouseProductFilter
from apps.warehouse.filters import WarehouseProductFilter as OnlineWarehouseProductFilter
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse products',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class OfflineWarehouseProductListAPIView(ListAPIView):
    queryset = OfflineWarehouseProduct.objects.all()
    serializer_class = OfflineWarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]

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

    def get_filterset_class(self):
        if global_state.get():
            return OnlineWarehouseProductFilter
        else:
            return WarehouseProductFilter

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(WarehouseProduct.objects.all())
                serializer = WarehouseProductGetSerializer
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


@extend_schema(tags=["Offline WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse product',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class OfflineWarehouseProductRetrieveAPIView(RetrieveAPIView):
    queryset = OfflineWarehouseProduct.objects.all()
    serializer_class = OfflineWarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, pk):
        try:
            if global_state.get():
                query = WarehouseProduct.objects.filter(pk=pk).first()
                serializer = WarehouseProductGetSerializer
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


@extend_schema(tags=["Offline WarehouseProduct"])
@extend_schema_view(
    post=extend_schema(
        summary='create warehouse product',
        description='Permission: admin, warehouse_writer'
    )
)
class OfflineWarehouseProductCreateAPIView(CreateAPIView):
    queryset = OfflineWarehouseProduct.objects.all()
    serializer_class = OfflineWarehouseProductPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user
            if global_state.get():
                serializer = WarehouseProductPostSerializer(data=request.data)
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


@extend_schema(tags=["Offline WarehouseProduct"])
@extend_schema_view(
    post=extend_schema(
        summary='create warehouse product by barcode',
        description='Permission: admin, warehouse_writer'
    )
)
class OfflineWarehouseProductCreateByBarcodeAPIView(CreateAPIView):
    queryset = OfflineWarehouseProduct.objects.all()
    serializer_class = OfflineWarehouseProductBarcodeSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user
            if global_state.get():
                serializer = WarehouseProductBarcodeSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    instance = serializer.save()
                    return Response(OfflineWarehouseProductGetSerializer(instance).data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    instance = serializer.save()
                    return Response(OfflineWarehouseProductGetSerializer(instance).data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse product',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update warehouse product',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='partial update warehouse product',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete warehouse product',
        description='Permission: admin, warehouse_writer'
    )
)
class OfflineWarehouseProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = OfflineWarehouseProduct.objects.all()
    serializer_class = OfflineWarehouseProductPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, pk):
        try:
            if global_state.get():
                query = WarehouseProduct.objects.filter(pk=pk).first()
                serializer = WarehouseProductPostSerializer
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
            request.data['user'] = request.user
            if global_state.get():
                query = WarehouseProduct.objects.filter(pk=pk).first()
                serializer = WarehouseProductPostSerializer(query, data=request.data)
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
            request.data['user'] = request.user
            if global_state.get():
                query = WarehouseProduct.objects.filter(pk=pk).first()
                serializer = WarehouseProductPostSerializer(query, data=request.data, partial=True)
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
                query = WarehouseProduct.objects.filter(pk=pk).first()
                if query:
                    query.delete()
                    return Response({'message': 'deleted'}, status=204)
                return Response({'error': 'not found'}, status=404)
            else:
                query = self.queryset.filter(pk=pk).first()
                if query:
                    query.delete()
                    return Response({'message': 'deleted'}, status=204)
                return Response({'error': 'not found'}, status=404)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
