from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Colors
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator
from rest_framework import status
from rest_framework.response import Response


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get colors',
        description="description='Permission: admin, strih"
    )
)
class ColorsListView(ListAPIView):
    """
    API endpoint that allows colors to be viewed.

    Supports filtering by:
    - id (exact match)
    - color_code (exact match)
    - russian_title (contains match)

    Returns paginated results using standard Bloom pagination format.
    """
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'color_code', 'russian_title')


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get colors by model_name.id',
        description='Permission: admin, strih',
        parameters=[
            OpenApiParameter(
                name='model_name_id',
                location=OpenApiParameter.QUERY,
                description='model_name.id',
                required=True,
                type=int,
            ),
        ],
    )
)
class ColorsByModelNameListView(ListAPIView):
    """
    API endpoint that returns colors available for a specific model name.

    Requires model_name_id query parameter.
    Returns paginated results using standard Bloom pagination format.
    """
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator

    def get(self, request):
        model_name_id = request.query_params.get('model_name_id', None)
        if not model_name_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'model_name_id not fount'}
            )
        queryset = Colors.objects.filter(modelcolors__model_id__name_id=model_name_id).distinct()
        page = self.paginate_queryset(queryset)
        serializer = ColorsSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
