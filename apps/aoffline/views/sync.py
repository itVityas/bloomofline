from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.aoffline.utils.aoffline_sync import AccountSynchronization


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start synchronization account models from mssql to offline',
        description='1',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class SyncAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        acc_sync = AccountSynchronization()
        acc_sync.full_sync()
        return Response({'status': 'ok'})
