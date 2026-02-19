from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Products
# from apps.sez.models import ClearanceInvoice
from apps.ashtrih.serializers.products import ProductGetSerializer, ProductUpdateClearedSerializer
from apps.ashtrih.permission import StrihPermission
from apps.ashtrih.filterset import ProductFilter


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


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    patch=extend_schema(
        summary='Partial update Products cleared',
        description="description='Permission: admin, strih",
    ),
    put=extend_schema(
        summary='Full update Products cleared',
        description="description='Permission: admin, strih",
    )
)
class ProductUpdateClearedView(UpdateAPIView):
    """
    API endpoint that allows clearing of products.

    This endpoint is used to update the 'cleared' field of a product.
    It requires authentication and specific permissions.

    Typical filters include:
    - barcode: Exact barcode match
    - state: Product condition/state
    - model: Filter by specific model
    - color_id: Filter by color
    - search: Search across multiple fields
    """
    queryset = Products.objects.all()
    serializer_class = ProductUpdateClearedSerializer
    permission_classes = (IsAuthenticated, StrihPermission)

    def perform_update(self, serializer: ProductUpdateClearedSerializer):
        clearance_invoice_id = self.request.data.get('cleared', None)
        if clearance_invoice_id is None:
            serializer.save(cleared=None)
        # else:
            # clearance_invoice = ClearanceInvoice.objects.filter(
            #     pk=clearance_invoice_id
            # ).first()
            # serializer.save(cleared=clearance_invoice)
