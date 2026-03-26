from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.ashtrih.models import OfflineModelNames, OfflineModels, OfflineProducts
from apps.shtrih.models import Products, Models, ModelNames
from apps.ashtrih.serializers.model_name import OfflineModelNamesSerializer, OfflineCountSerializer
from apps.ashtrih.permission import StrihPermission
from bloomofline.paginator import StandartResultPaginator
from apps.ashtrih.filterset import ModelNamesFilter
from apps.shtrih.filterset import ModelNamesFilter as OnlineModelNamesFilter
from bloomofline.global_state import global_state


@extend_schema(tags=['Offline Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model',
        description="description='Permission: admin, strih"
    )
)
class OfflineModelNameListView(ListAPIView):
    """
    API endpoint that allows model names to be viewed.

    Supports filtering by:
    - id (exact match)
    - name (contains match)
    - short_name (exact match)

    Returns paginated results using standard Bloom pagination format.
    """
    queryset = OfflineModelNames.objects.all()
    serializer_class = OfflineModelNamesSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelNamesFilter

    def get_filterset_class(self):
        if global_state.get():
            return OnlineModelNamesFilter
        else:
            return ModelNamesFilter

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
                query = self.filter_queryset(ModelNames.objects.all())
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


@extend_schema(tags=['Offline Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='count product by model_name.id',
        description="description='Permission: admin, strih",
    ),
)
class OfflineProductCountByModelNameView(APIView):
    """
    API endpoint that returns product count for a specific model name.

    Returns:
    - count: Number of products for the model
    - code: Internal model code (0 if model not found)
    """
    permission_classes = (IsAuthenticated, StrihPermission)
    serializer_class = OfflineCountSerializer

    def get(self, request, pk):
        try:
            if global_state.get():
                count = Products.objects.filter(model__name_id=pk).exclude(state=1).count()
                model = Models.objects.filter(name_id=pk).first()
            else:
                count = OfflineProducts.objects.filter(model__name_id=pk).exclude(state=1).count()
                model = OfflineModels.objects.filter(name_id=pk).first()
            model_code = 0
            if model:
                model_code = model.code
            return Response({'count': count, 'code': model_code})
        except Exception as e:
            global_state.set()
            return Response({'error': str(e)})
