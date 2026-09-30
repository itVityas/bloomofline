from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from django.db.models.functions import Now
from django.db import connection, transaction
import logging

from apps.aoffline.utils.aoffline_sync import AccountFullSynchronization, AccountSync
from apps.aonec.utils.aonec_sync import OneCFullSync, OneCSync
from apps.ashtrih.utils.ashtrih_sync import ShtrihFullSync, ShtrihSync
from apps.woffline.utils.woffline_sync import WarehouseFullSync, WarehouseSync
from apps.osgp.utils.osgp_sync import SGPFullSync, SGPSync
from apps.sync.models import SyncDate
from bloomofline.db_routers import ModelDatabaseRouter
from apps.warehouse.models import WarehouseAction


logger = logging.getLogger(__name__)


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start full synchronization all app. Without sync!',
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
            if ModelDatabaseRouter().check_mssql_connection() is False:
                return Response({'error': 'No connect db'}, status=400)
            sync_date = SyncDate.objects.all().order_by('-last_sync').first()
            if not sync_date:
                sync_date = SyncDate(last_sync='1970-01-01 00:00:00')
            server_time = WarehouseAction.objects.annotate(current_time=Now()).first().current_time

            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys = OFF;")
                cursor.execute("PRAGMA journal_mode = MEMORY;")
                cursor.execute("PRAGMA synchronous = OFF;")
                cursor.execute("PRAGMA cache_size = -64000;")
                cursor.execute("PRAGMA temp_store = MEMORY;")

                try:
                    with transaction.atomic():
                        cursor.execute("""
                            SELECT name FROM sqlite_master
                            WHERE type='table'
                            AND name NOT LIKE 'django_%';
                        """)
                        tables = [row[0] for row in cursor.fetchall()]
                        for table in tables:
                            cursor.execute(f"DELETE FROM {table};")
                        cursor.execute("DELETE FROM sqlite_sequence;")
                except Exception as e:
                    logger.error(f"Error deleting data: {e}")

                with transaction.atomic():
                    time_account = AccountFullSynchronization().full_sync()
                    time_shtrih = ShtrihFullSync(sync_date=sync_date).full_sync()
                    time_ttn = OneCFullSync(sync_date=sync_date).full_sync()
                    time_warehouse = WarehouseFullSync(sync_date=sync_date).full_sync()
                    time_sgp = SGPFullSync(sync_date=sync_date).full_sync()
                    full_time = time_account.get('full', 0) + time_shtrih.get('full', 0) \
                        + time_ttn.get('full', 0) + time_warehouse.get('full', 0) \
                        + time_sgp.get('full', 0)
                    new_sync_date = SyncDate(last_sync=server_time)
                    new_sync_date.save()

                cursor.execute("PRAGMA foreign_keys = ON;")
                cursor.execute("PRAGMA journal_mode = WAL;")
                cursor.execute("PRAGMA synchronous = NORMAL;")

            return Response({
                'account': time_account,
                'onec': time_ttn,
                'shtrih': time_shtrih,
                'warehouse': time_warehouse,
                'sgp': time_sgp,
                'full_time': full_time,
                'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


@extend_schema(tags=['Synchronization'])
@extend_schema_view(
    get=extend_schema(
        summary='Start synchronization from mssql to offline',
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
            if ModelDatabaseRouter().check_mssql_connection() is False:
                return Response({'error': 'No connect db'}, status=400)
            sync_date = SyncDate.objects.all().order_by('-last_sync').first()
            if not sync_date:
                sync_date = SyncDate(last_sync='1970-01-01 00:00:00')
            server_time = WarehouseAction.objects.annotate(current_time=Now()).first().current_time

            with connection.cursor() as cursor:
                cursor.execute("PRAGMA journal_mode = WAL;")
                cursor.execute("PRAGMA synchronous = NORMAL;")   # НЕ OFF — для инкремента
                cursor.execute("PRAGMA busy_timeout = 5000;")    # ждать блокировки
                cursor.execute("PRAGMA temp_store = MEMORY;")
                cursor.execute("PRAGMA cache_size = -64000;")
                cursor.execute("PRAGMA wal_autocheckpoint = 1000;")
                cursor.execute("PRAGMA foreign_keys = ON;")

                time_account = AccountSync().sync()
                time_shtrih = ShtrihSync(sync_date=sync_date).sync()
                time_ttn = OneCSync(sync_date=sync_date).sync()
                time_warehouse = WarehouseSync(sync_date=sync_date).sync()
                time_sgp = SGPSync(sync_date=sync_date).sync()
                full_time = time_account.get('full', 0) + time_shtrih.get('full', 0) \
                    + time_ttn.get('full', 0) + time_warehouse.get('full', 0) \
                    + time_sgp.get('full', 0)
                new_sync_date = SyncDate(last_sync=server_time)
                new_sync_date.save()
            return Response({
                'account': time_account,
                'onec': time_ttn,
                'shtrih': time_shtrih,
                'warehouse': time_warehouse,
                'sgp': time_sgp,
                'full_time': full_time,
                'status': 'ok'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
