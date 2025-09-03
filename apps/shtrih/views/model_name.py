from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

from apps.shtrih.models import ModelNames, Models, Products
from apps.shtrih.serializers.model_name import ModelNamesSerializer, CountSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model',
        description="description='Permission: admin, strih"
    )
)
class ModelNameListView(ListAPIView):
    """
    API endpoint that allows model names to be viewed.

    Supports filtering by:
    - id (exact match)
    - name (contains match)
    - short_name (exact match)

    Returns paginated results using standard Bloom pagination format.
    """
    queryset = ModelNames.objects.all()
    serializer_class = ModelNamesSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'name', 'short_name')


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model by product_code',
        description="description='Permission: admin, strih",
        parameters=[
            OpenApiParameter(
                name='production_code_id',
                location=OpenApiParameter.QUERY,
                description='production_code.id',
                required=True,
                type=int,
            ),
        ],
    )
)
class ModelNameByProductCodeListView(ListAPIView):
    """
    API endpoint that returns model names filtered by production code.

    Requires production_code_id query parameter.
    Returns paginated results using standard Bloom pagination format.
    """
    queryset = ModelNames.objects.all()
    serializer_class = ModelNamesSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'name', 'short_name')

    def get(self, request):
        production_code_id = request.query_params.get('production_code_id', None)
        if not production_code_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'product_code not fount'}
            )
        queryset = ModelNames.objects.filter(models__production_code=production_code_id)
        page = self.paginate_queryset(queryset)
        serializer = ModelNamesSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='count product by model_name.id',
        description="description='Permission: admin, strih",
    ),
)
class ProductCountByModelNameView(APIView):
    """
    API endpoint that returns product count for a specific model name.

    Returns:
    - count: Number of products for the model
    - code: Internal model code (0 if model not found)
    """
    permission_classes = (IsAuthenticated, StrihPermission)
    serializer_class = CountSerializer

    def get(self, request, pk):
        count = Products.objects.filter(model__name_id=pk).count()
        model = Models.objects.filter(name_id=pk).first()
        model_code = 0
        if model:
            model_code = model.code
        return Response({'count': count, 'code': model_code})
