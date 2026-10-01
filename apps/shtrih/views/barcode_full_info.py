from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework import status

from apps.shtrih.serializers.barcode_full_info import BarcodeInfoSerializer
from apps.shtrih.models import Products


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        description='Get full info about barcode, online',
        parameters=[
            OpenApiParameter(
                    name='barcode',
                    location=OpenApiParameter.QUERY,
                    description='barcode',
                    required=True,
                    type=str
                )
        ],
        responses={
            200: BarcodeInfoSerializer,
            400: OpenApiResponse(description='Bad request'),
            }
    )
)
class BarcodeFullInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BarcodeInfoSerializer

    def get(self, request):
        try:
            barcode = request.query_params.get('barcode')
            if not barcode:
                return Response({'error': 'Barcode is required'}, status=status.HTTP_400_BAD_REQUEST)
            product = Products.objects.filter(barcode=barcode).first()
            if not product:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = BarcodeInfoSerializer(
                data={'barcode': barcode},
                many=False)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
