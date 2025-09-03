import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse)

from django.conf import settings


@extend_schema(tags=['1c'])
@extend_schema_view(
    get=extend_schema(
        summary='get weight from 1c',
        description='Permission: auth user',
        parameters=[
            OpenApiParameter(
                name='model_name',
                description='model name',
                required=True,
                type=str
            ),
        ],
        responses={
            200: OpenApiResponse(description="json from 1C"),
            400: OpenApiResponse(description="Missing required parameters"),
        }
    ),
)
class Weight1cView(APIView):
    """
    API endpoint for retrieving product weight information from 1C ERP system.

    This view:
    - Accepts a model name parameter
    - Makes authenticated request to 1C web service
    - Returns the weight information
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET request to fetch weight from 1C.

        Args:
            request: HTTP request containing 'model_name' query parameter

        Returns:
            Response with weight data or error message
        """
        model_name = request.query_params.get('model_name', None)
        if not model_name:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        url = f'http://192.168.2.2/OLYA/hs/bloom/weight?model={model_name}'
        response = requests.get(
            url,
            auth=(settings.API_USERNAME, settings.API_PASSWORD),
            timeout=30
        )
        if response.status_code != 200:
            return Response({'error': 'Bad response from 1C'})
        return Response(response.json(), status=status.HTTP_200_OK)
