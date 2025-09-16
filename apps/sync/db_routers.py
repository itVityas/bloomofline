class ModelDatabaseRouter:
    route_app_labels = {"apps.sync"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "local"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "local"
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'local':
            return True
        return False
