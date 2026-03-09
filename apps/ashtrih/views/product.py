from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.ashtrih.models import OfflineProducts
from apps.shtrih.models import Products
from apps.ashtrih.serializers.products import OfflineProductGetSerializer
from apps.ashtrih.permission import StrihPermission
from apps.ashtrih.filterset import ProductFilter
from bloomofline.global_state import global_state
from rest_framework.response import Response


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

    def get(self, request):
        try:
            if global_state.get():
                query = Products.objects.all()
                serializer = self.serializer_class
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.queryset
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
        except Exception as e:
            global_state.get()
            return Response({'error': str(e)})
