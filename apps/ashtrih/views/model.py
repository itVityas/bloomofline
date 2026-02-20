from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.ashtrih.models import OfflineModels
from apps.ashtrih.serializers.model import OfflineModelsSerializer
from apps.ashtrih.permission import StrihPermission
from bloomofline.paginator import StandartResultPaginator
from apps.ashtrih.filterset import ModelFilter


@extend_schema(tags=['Offline Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model',
        description="description='Permission: admin, strih"
    )
)
class OfflineModelListView(ListAPIView):
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
    queryset = OfflineModels.objects.all()
    serializer_class = OfflineModelsSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter
