from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.ashtrih.utils.ashtrih_sync import ShtrihFullSync, ShtrihSync
from apps.sync.models import SyncDate


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start full synchronization shtrih models from mssql to offline',
        description='1',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class SyncFullStrihView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sync_date = SyncDate.objects.all().order_by('-last_sync').first()
            if not sync_date:
                sync_date = SyncDate(last_sync='1970-01-01 00:00:00')
            acc_sync = ShtrihFullSync(sync_date=sync_date)
            acc_sync.full_sync()
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)})


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start synchronization shtrih models from mssql to offline',
        description='1',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class SyncShtrihView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sync_date = SyncDate.objects.all().order_by('-last_sync').first()
            if not sync_date:
                sync_date = SyncDate(last_sync='1970-01-01 00:00:00')
            acc_sync = ShtrihSync(sync_date=sync_date)
            acc_sync.sync()
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)})
