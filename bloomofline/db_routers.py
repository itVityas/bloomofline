import logging

from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class ModelDatabaseRouter:
    route_app_labels = {
        "account": 'bloom',
        "onec": 'bloom',
        "shtrih": 'bloom',
        "warehouse": 'bloom',
        "sync": 'default',
        'aoffline': 'default',
        'aonec': 'default',
        'ashtrih': 'default'
        }

    def check_mssql_connection(self):
        """
        Проверяет доступность MSSQL базы данных
        """
        try:
            # Пробуем выполнить простой запрос к MSSQL
            with connections['bloom'].cursor() as cursor:
                cursor.execute("SET LOCK_TIMEOUT 2000;")
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except OperationalError as e:
            logger.info(f"MSSQL connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error checking MSSQL: {e}")
            return False

    def db_for_read(self, model, **hints):
        if self.route_app_labels.get(model._meta.app_label, None) is not None:
            return self.route_app_labels.get(model._meta.app_label, None)
        return None

    def db_for_write(self, model, **hints):
        if self.route_app_labels.get(model._meta.app_label, None) is not None:
            return self.route_app_labels.get(model._meta.app_label, None)
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels and self.route_app_labels.get(app_label, None) == 'default':
            return db == self.route_app_labels[app_label]
        if app_label in self.route_app_labels and self.route_app_labels.get(app_label, None) == 'bloom':
            return False
        return db == 'default'
