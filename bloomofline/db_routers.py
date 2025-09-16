class ModelDatabaseRouter:
    def db_for_read(self, model, **hints):
        return self._get_db_for_model(model)

    def db_for_write(self, model, **hints):
        return self._get_db_for_model(model)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default':
            return False
        return True

    def _get_db_for_model(self, model):
        if hasattr(model._meta, 'using_db'):
            return model._meta.using_db
        return 'default'
