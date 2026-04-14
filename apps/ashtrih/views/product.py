from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.ashtrih.models import OfflineProducts
from apps.shtrih.models import Products
from apps.ashtrih.serializers.products import OfflineProductGetSerializer, OnlineProductGetSerializer
from apps.ashtrih.permission import StrihPermission
from apps.ashtrih.filterset import ProductFilter
from apps.shtrih.filterset import ProductFilter as OnlineProductFilter
from bloomofline.global_state import global_state
from rest_framework.response import Response
from bloomofline.paginator import StandartResultPaginator


@extend_schema(tags=['Offline Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List of Products',
        description="description='Permission: admin, strih",
    )
)
class OfflineProductListView(ListAPIView):
    """
    API endpoint that allows products to be viewed with their complete details.

    Provides:
    - Full product information including nested color and model data
    - Advanced filtering capabilities
    - Search functionality
    - Standard pagination

    Typical filters include:
    - barcode: Exact barcode match
    - state: Product condition/state
    - model: Filter by specific model
    - color_id: Filter by color
    - search: Search across multiple fields
    """
    queryset = OfflineProducts.objects.all()
    serializer_class = OfflineProductGetSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = StandartResultPaginator

    def get_filterset_class(self):
        if global_state.get():
            return OnlineProductFilter
        else:
            return ProductFilter

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
                query = self.filter_queryset(Products.objects.all())
                serializer = OnlineProductGetSerializer
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
