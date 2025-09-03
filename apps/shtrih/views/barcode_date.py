from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter)

from apps.shtrih.models import Protocols
from apps.shtrih.serializers.protocols import ProtocolsFullSerializer
from apps.shtrih.permission import StrihPermission


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='get date from barcode number',
        description="description='Permission: admin, strih",
        parameters=[
            OpenApiParameter(
                name='barcode',
                location=OpenApiParameter.QUERY,
                description='barcode',
                required=True,
                type=str,
            )
        ],
        responses={
            200: ProtocolsFullSerializer,
            400: OpenApiResponse(description='Bad request'),
            401: OpenApiResponse(description='Unauthorized'),
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Not found'),
        }
    )
)
class DateFromBarcodeView(APIView):
    serializer_class = ProtocolsFullSerializer
    queryset = Protocols.objects.all()
    permission_classes = (IsAuthenticated, StrihPermission,)

    def get(self, request):
        barcode = request.query_params.get('barcode', None)
        if not barcode:
            return Response({'error': 'barcode is required'}, status=status.HTTP_400_BAD_REQUEST)
        protocols = Protocols.objects.filter(product__barcode=barcode)
        if not protocols:
            return Response({'error': 'barcode not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProtocolsFullSerializer(protocols, many=True).data, status=status.HTTP_200_OK)
