from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.aoffline.utils.aoffline_sync import AccountFullSynchronization
from apps.aonec.utils.aonec_sync import OneCFullSync, OneCSync
from apps.ashtrih.utils.ashtrih_sync import ShtrihFullSync, ShtrihSync


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start full synchronization all app',
        description='All delete and then all download',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class FullSyncAllView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            AccountFullSynchronization().full_sync()
            OneCFullSync().full_sync()
            ShtrihFullSync().full_sync()
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start synchronization account models from mssql to offline',
        description='Sync all  that older then field update_at',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class SyncAllView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            AccountFullSynchronization().full_sync()
            OneCSync().sync()
            ShtrihSync().sync()
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
