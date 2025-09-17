class ModelDatabaseRouter:
    route_app_labels = {
        "account": 'bloom',
        "onec": 'bloom',
        "shtrih": 'bloom',
        "warehouse": 'bloom',
        "sync": 'default'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "default"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "default"
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default':
            return False
        return False
