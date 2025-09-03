from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Production_codes
from apps.shtrih.serializers.production_code import ProductionCodeSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List production_code',
        description="description='Permission: admin, strih"
    )
)
class ProductionCodeListView(ListAPIView):
    """
    API endpoint that allows production codes to be viewed.

    Provides:
    - Complete list of production codes with their details
    - Filtering capabilities by code, name, and nameplate requirement
    - Search functionality across code numbers and names
    - Standard pagination

    Each production code includes:
    - Unique code number
    - Descriptive name
    - Nameplate requirement flag
    - Formatted code (string representation)
    """
    permission_classes = (IsAuthenticated, StrihPermission)
    serializer_class = ProductionCodeSerializer
    queryset = Production_codes.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code', 'name', 'nameplate']
