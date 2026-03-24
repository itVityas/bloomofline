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
    WarehouseDoPalletSerializer
)
from apps.woffline.serializers.warehouse_do import (
    OfflineWarehouseDoGetSerializer,
    OfflineWarehouseDoPostSerializer,
    OfflineWarehouseDoPalletSerializer
)
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from apps.woffline.filters import WarehouseDoFilter
from apps.warehouse.filters import WarehouseDoFilter as OnlineWarehouseDoFilter
from bloomofline.global_state import global_state


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse do',
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
    post=extend_schema(
        summary='Create a new WarehouseDo',
        description='Permission: admin, warehouse_writer',
    )
)
class OfflineWarehouseDoCreateAPIView(CreateAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = WarehouseDoPostSerializer(data=request.data)
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
            request.data['user'] = request.user.id
            if global_state.get():
                query = WarehouseDo.objects.filter(pk=pk).first()
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
            request.data['user'] = request.user.id
            if global_state.get():
                query = WarehouseDo.objects.filter(pk=pk).first()
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


@extend_schema(tags=["Offline WarehouseDo"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a WarehouseDo by barcode in pallet',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineWarehouseDoBarcodePalletAPIView(CreateAPIView):
    queryset = OfflineWarehouseDo.objects.all()
    serializer_class = OfflineWarehouseDoPalletSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = WarehouseDoPalletSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
