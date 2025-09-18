class ModelDatabaseRouter:
    route_app_labels = {
        "account": 'bloom',
        "onec": 'bloom',
        "shtrih": 'bloom',
        "warehouse": 'bloom',
        "sync": 'default',
        'aoffline': 'default'}

    def db_for_read(self, model, **hints):
        if not self.route_app_labels.get(model._meta.app_label, None):
            return self.route_app_labels.get(model._meta.app_label, None)
        return None

    def db_for_write(self, model, **hints):
        if not self.route_app_labels.get(model._meta.app_label, None):
            return self.route_app_labels.get(model._meta.app_label, None)
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == self.route_app_labels[app_label]
        return None
