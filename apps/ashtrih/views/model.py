from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.ashtrih.models import OfflineModels
from apps.shtrih.models import Models
from apps.ashtrih.serializers.model import OfflineModelsSerializer
from apps.ashtrih.permission import StrihPermission
from bloomofline.paginator import StandartResultPaginator
from apps.ashtrih.filterset import ModelFilter
from apps.shtrih.filterset import ModelFilter as OnlineModelFilter
from bloomofline.global_state import global_state


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

    def get_filterset_class(self):
        if global_state.get():
            return OnlineModelFilter
        else:
            return ModelFilter

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
                query = self.filter_queryset(Models.objects.all())
                serializer = self.serializer_class
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
            else:
                serializer = self.serializer_class
                query = self.filter_queryset(self.queryset)
                page = self.paginate_queryset(query)
                return self.get_paginated_response(serializer(page, many=True).data)
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)})
