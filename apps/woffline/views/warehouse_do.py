from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.warehouse.models import WarehouseDo
from apps.woffline.models import OfflineWarehouseDo
from apps.warehouse.serializers.warehouse_do import (
    WarehouseDoGetSerializer,
    WarehouseDoPostSerializer,
    WarehouseDoBarcodeSerializer,
    WarehouseDoPalletSerializer,
    WarehouseDoShipmentSerializer
)
from apps.woffline.serializers.warehouse_do import (
    OfflineWarehouseDoGetSerializer,
    OfflineWarehouseDoPostSerializer,
    OfflineWarehouseDoBarcodeSerializer,
    OfflineWarehouseDoPalletSerializer,
    OfflineWarehouseDoShipmentSerializer
)
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from apps.woffline.filters import WarehouseDoFilter
from apps.warehouse.filters import WarehouseDoFilter as OnlineWarehouseDoFilter
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='Get list warehouse do with filters',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineWarehouseDoListAPIView(ListAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseDoFilter

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
            return OnlineWarehouseDoFilter
        else:
            return WarehouseDoFilter

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(WarehouseDo.objects.all())
                serializer = WarehouseDoGetSerializer
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


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseDo',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    patch=extend_schema(
        summary='Update a WarehouseDo',
        description='Permission: admin warehouse_writer',
    ),
    put=extend_schema(
        summary='Update a WarehouseDo',
        description='Permission: admin warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete a WarehouseDo',
        description='Permission: admin warehouse_writer',
    ),
)
class OfflineWarehouseDoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, pk):
        try:
            if global_state.get():
                query = WarehouseDo.objects.filter(pk=pk).first()
                serializer = WarehouseDoPostSerializer
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
            request.data['user'] = request.user.id
            if global_state.get():
                query = WarehouseDo.objects.filter(pk=pk).first()
                serializer = WarehouseDoPostSerializer(query, data=request.data)
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
            request.data['user'] = request.user.id
            if global_state.get():
                query = WarehouseDo.objects.filter(pk=pk).first()
                serializer = WarehouseDoPostSerializer(query, data=request.data, partial=True)
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
                query = WarehouseDo.objects.filter(pk=pk).first()
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


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseDo',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineWarehouseDoRetrieveAPIView(RetrieveAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, pk):
        try:
            if global_state.get():
                query = WarehouseDo.objects.filter(pk=pk).first()
                serializer = WarehouseDoGetSerializer
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


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a WarehouseDo by product barcode',
        description='''Permission: admin, warehouse, warehouse_writer
        product barcode and add it to warhouse_ttn, if not warehouse_ttn create it
        not for shipment and palleting operations ''',
    ),
)
class OfflineWarehouseDoBarcodeAPIView(CreateAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoBarcodeSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = WarehouseDoBarcodeSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    do = serializer.save()
                    return Response(WarehouseDoGetSerializer(do).data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    do = serializer.save()
                    return Response(OfflineWarehouseDoGetSerializer(do).data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a WarehouseDo by product barcode for palleting',
        description='''Permission: admin, warehouse, warehouse_writer
        product barcode and add it to warhouse_ttn, if not warehouse_ttn create it
        only for palleting operations ''',
    ),
)
class OfflineWarehouseDoPalletAPIView(CreateAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoPalletSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = WarehouseDoPalletSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    do = serializer.save()
                    return Response(WarehouseDoGetSerializer(do).data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    do = serializer.save()
                    return Response(OfflineWarehouseDoGetSerializer(do).data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a WarehouseDo by product barcode for shipment',
        description='''Permission: admin, warehouse, warehouse_writer
        product barcode and add it to warhouse_ttn, if not warehouse_ttn create it
        only for shipment operations ''',
    ),
)
class OfflineWarehouseDoShipmentAPIView(CreateAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoShipmentSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = WarehouseDoShipmentSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    do = serializer.save()
                    return Response(WarehouseDoGetSerializer(do).data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    do = serializer.save()
                    return Response(OfflineWarehouseDoGetSerializer(do).data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
