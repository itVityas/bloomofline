from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse
)
from rest_framework.response import Response
from rest_framework import status

from apps.warehouse.models import WarehouseTTN, WarehouseDo
from apps.woffline.models import OfflineWarehouseTTN, OfflineWarehouseDo
from apps.warehouse.serializers.warehouse_ttn import (
    WarehouseTTNPostSerializer,
    WarehouseTTNGetSerializer,
    WarehouseTTNProductSerializer
)
from apps.woffline.serializers.warehouse_ttn import (
    OfflineWarehouseTTNGetSerializer,
    OfflineWarehouseTTNPostSerializer,
    OfflineWarehouseTTNProductSerializer,
)
from apps.woffline.permissions import WarehousePermission
from bloomofline.paginator import StandartResultPaginator
from apps.woffline.filters import WarehouseTTNFilter
from apps.warehouse.filters import WarehouseTTNFilter as OnlineWarehouseTTNFilter
from bloomofline.global_state import global_state


@extend_schema(tags=['Offline WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get all WarehouseTTN',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineWarehouseTTNListAPIView(ListAPIView):
    queryset = OfflineWarehouseTTN.objects.all()
    serializer_class = OfflineWarehouseTTNGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseTTNFilter

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
            return OnlineWarehouseTTNFilter
        else:
            return WarehouseTTNFilter

    def get(self, request):
        try:
            if global_state.get():
                query = self.filter_queryset(WarehouseTTN.objects.all())
                serializer = WarehouseTTNGetSerializer
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


@extend_schema(tags=['Offline WarehouseTTN'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new WarehouseTTN',
        description='Permission: admin, warehouse_writer',
    )
)
class OfflineWarehouseTTNCreateAPIView(CreateAPIView):
    queryset = OfflineWarehouseTTN.objects.all()
    serializer_class = OfflineWarehouseTTNPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                serializer = WarehouseTTNPostSerializer(data=request.data)
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


@extend_schema(tags=['Offline WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseTTN',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    put=extend_schema(
        summary='Update a WarehouseTTN',
        description='Permission: admin warehouse_writer',
    ),
    patch=extend_schema(
        summary='partial update a WarehouseTTN',
        description='Permission: admin warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete a WarehouseTTN',
        description='Permission: admin, warehouse_writer',
    )
)
class OfflineWarehouseTTNRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OfflineWarehouseTTN.objects.all()
    serializer_class = OfflineWarehouseTTNPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, ttn_number):
        try:
            if global_state.get():
                query = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
                serializer = WarehouseTTNPostSerializer
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = self.queryset.filter(ttn_number=ttn_number).first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)

    def put(self, request, ttn_number):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                query = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
                serializer = WarehouseTTNPostSerializer(query, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                query = self.queryset.filter(ttn_number=ttn_number).first()
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

    def patch(self, request, ttn_number):
        try:
            request.data['user'] = request.user.id
            if global_state.get():
                query = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
                serializer = WarehouseTTNPostSerializer(query, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                query = self.queryset.filter(ttn_number=ttn_number).first()
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

    def delete(self, request, ttn_number):
        try:
            if global_state.get():
                query = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
                if query:
                    warehouse_do = WarehouseDo.objects.filter(warehouse_ttn=query)
                    warehouse_do.delete()
                    query.delete()
                    return Response({'message': 'deleted'}, status=204)
                return Response({'error': 'not found'}, status=404)
            else:
                query = self.queryset.filter(ttn_number=ttn_number).first()
                if query:
                    warehouse_do = OfflineWarehouseDo.objects.filter(warehouse_ttn=query)
                    warehouse_do.delete()
                    query.delete()
                    return Response({'message': 'deleted'}, status=204)
                return Response({'error': 'not found'}, status=404)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=["Offline WarehouseTTN"])
@extend_schema_view(
    get=extend_schema(
        summary='Get detailed WarehouseTTN by id',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineWarehouseTTNRetrieveAPIView(RetrieveAPIView):
    queryset = OfflineWarehouseTTN.objects.all()
    serializer_class = OfflineWarehouseTTNGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def get(self, request, ttn_number):
        try:
            if global_state.get():
                query = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
                serializer = WarehouseTTNGetSerializer
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = self.queryset.filter(ttn_number=ttn_number).first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=['Offline WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get latest WarehouseTTN by user_id',
        description='Permission: admin, warehouse, warehouse_writer',
        parameters=[
            OpenApiParameter(
                name='user_id',
                description='User ID',
                required=True,
                type=int
            )
        ],
        responses={
            200: OfflineWarehouseTTNGetSerializer,
            404: OpenApiResponse(description='WarehouseTTN not found')
        },
    ),
)
class OfflineWarehouseTTNByUserIdAPIView(APIView):
    permission_classes = [IsAuthenticated, WarehousePermission]
    serializer_class = OfflineWarehouseTTNGetSerializer

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                return Response(
                    {'error': 'user_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            if global_state.get():
                query = WarehouseTTN.objects.filter(user_id=user_id).order_by('-create_at').first()
                serializer = WarehouseTTNGetSerializer
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = OfflineWarehouseTTN.objects.filter(user_id=user_id).order_by('-create_at').first()
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=['Offline WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get WarehouseTTN products by ttn_number',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class OfflineWarehouseTTNProductsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, WarehousePermission]
    serializer_class = OfflineWarehouseTTNProductSerializer
    queryset = OfflineWarehouseTTN.objects.all()

    def get(self, request, ttn_number):
        try:
            if global_state.get():
                query = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
                serializer = WarehouseTTNProductSerializer
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = self.queryset.filter(ttn_number=ttn_number).first()
                if not query:
                    return Response({'error': 'not found'}, status=404)
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=['Offline WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get latest WarehouseTTN with products by user_id',
        description='Permission: admin, warehouse, warehouse_writer',
        parameters=[
            OpenApiParameter(
                name='user_id',
                description='User ID',
                required=True,
                type=int
            )
        ],
        responses={
            200: OfflineWarehouseTTNGetSerializer,
            400: OpenApiResponse(description='WarehouseTTN not found')
        },
    ),
)
class OfflineWarehouseTTNProductsByUserIdAPIView(APIView):
    permission_classes = [IsAuthenticated, WarehousePermission]
    serializer_class = OfflineWarehouseTTNProductSerializer

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                return Response(
                    {'error': 'user_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            if global_state.get():
                query = WarehouseTTN.objects.filter(user_id=user_id).order_by('-create_at').first()
                serializer = WarehouseTTNProductSerializer
                return Response(serializer(query, many=False).data)
            else:
                serializer = self.serializer_class
                query = OfflineWarehouseTTN.objects.filter(user_id=user_id).order_by('-create_at').first()
                return Response(serializer(query, many=False).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)}, status=400)
