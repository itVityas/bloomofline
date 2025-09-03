from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Models
from apps.shtrih.serializers.model import ModelsSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model',
        description="description='Permission: admin, strih"
    )
)
class ModelListView(ListAPIView):
    """
    API endpoint that allows product models to be viewed with their full specifications.

    Supports:
    - Advanced filtering by various model attributes
    - Search across multiple fields
    - Pagination using standard Bloom format

    Typical filters include:
    - production_code: Filter by production line
    - name: Filter by model name
    - diagonal range: Filter by screen size
    - weight range: Filter by product weight
    """
    queryset = Models.objects.all()
    serializer_class = ModelsSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)
