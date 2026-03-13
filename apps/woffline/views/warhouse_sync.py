from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.woffline.utils.woffline_sync import WarehouseFullSync, WarehouseSync
from apps.sync.models import SyncDate


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start full synchronization warehouse models from mssql to offline',
        description='1',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class FullWarehouseSyncView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sync_date = SyncDate.objects.all().order_by('-last_sync').first()
            if not sync_date:
                sync_date = SyncDate(last_sync='1970-01-01 00:00:00')
            WarehouseFullSync(sync_date=sync_date).full_sync()
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start full synchronization warehouse models from mssql to offline',
        description='1',
        responses={
            200: OpenApiResponse(description='Synchronization ok'),
            400: OpenApiResponse(description='Bad synchronization'),
        }
    )
)
class WarehouseSyncView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sync_date = SyncDate.objects.all().order_by('-last_sync').first()
            if not sync_date:
                sync_date = SyncDate(last_sync='1970-01-01 00:00:00')
            WarehouseSync(sync_date=sync_date).sync()
            return Response({'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
