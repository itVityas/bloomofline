from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Products
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.shtrih.permission import StrihPermission
from apps.shtrih.filterset import ProductFilter


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List of Products',
        description="description='Permission: admin, strih",
    )
)
class ProductListView(ListAPIView):
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
    queryset = Products.objects.all()
    serializer_class = ProductGetSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
