from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from apps.warehouse.models import Shipment
from apps.woffline.models import OfflineShipment
from apps.warehouse.serializers.shipment import (
    ShipmentGetSerializer,
    ShipmentPostSerializer,
    ShipmentBarcodeSerializer
)
from apps.woffline.serializers.shipment import (
    OfflineShipmentGetSerializer,
    OfflineShipmentPostSerializer,
    OfflineShipmentBarcodeSerializer
)
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from apps.woffline.filters import ShipmentFilter
from apps.warehouse.filters import ShipmentFilter as OnlineShipmentFilter
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline Shipments"])
@extend_schema_view(
    post=extend_schema(
        summary='Create shipment',
        description='Permission: admin, warehouse_writer',
    ),
)
class OfflineShipmentCreateAPIView(CreateAPIView):
    queryset = OfflineShipment.objects.all()
    serializer_class = OfflineShipmentPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = ShipmentPostSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
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


@extend_schema(tags=["Offline Shipments"])
@extend_schema_view(
    get=extend_schema(
        summary='Get all shipments',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineShipmentListAPIView(ListAPIView):
    queryset = OfflineShipment.objects.all()
    serializer_class = OfflineShipmentGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filter_backends = [DjangoFilterBackend]
    pagination_class = StandartResultPaginator

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
            return OnlineShipmentFilter
        else:
            return ShipmentFilter

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(Shipment.objects.all())
                serializer = ShipmentGetSerializer
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


@extend_schema(tags=["Offline Shipments"])
@extend_schema_view(
    get=extend_schema(
        summary='Get shipment',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    put=extend_schema(
        summary='Update shipment',
        description='Permission: admin, warehouse_writer',
    ),
    patch=extend_schema(
        summary='Update shipment',
        description='Permission: admin, warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete shipment',
        description='Permission: admin, warehouse_writer',
    ),
)
class OfflineShipmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OfflineShipment.objects.all()
    serializer_class = OfflineShipmentPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, pk):
        try:
            if global_state.get():
                query = Shipment.objects.filter(pk=pk).first()
                serializer = ShipmentPostSerializer
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
                query = Shipment.objects.filter(pk=pk).first()
                serializer = ShipmentPostSerializer(query, data=request.data)
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
                query = Shipment.objects.filter(pk=pk).first()
                serializer = ShipmentPostSerializer(query, data=request.data, partial=True)
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
                query = Shipment.objects.filter(pk=pk).first()
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


@extend_schema(tags=["Offline Shipments"])
@extend_schema_view(
    get=extend_schema(
        summary='Get shipment',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineShipmentRetrieveAPIView(RetrieveAPIView):
    queryset = OfflineShipment.objects.all()
    serializer_class = OfflineShipmentGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, pk):
        try:
            if global_state.get():
                query = Shipment.objects.filter(pk=pk).first()
                serializer = ShipmentGetSerializer
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


@extend_schema(tags=["Offline Shipments"])
@extend_schema_view(
    post=extend_schema(
        summary='Get shipment by barcode',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineShipmentBarcodeRetrieveAPIView(CreateAPIView):
    queryset = OfflineShipment.objects.all()
    serializer_class = OfflineShipmentBarcodeSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = ShipmentBarcodeSerializer(data=request.data)
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
