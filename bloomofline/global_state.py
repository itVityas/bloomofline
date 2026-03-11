from django.core.cache import cache

from bloomofline.db_routers import ModelDatabaseRouter


class GlobalState:
    MSSQL_AVAILABLE = 'mssql_available'

    def __init__(self, update_interval=None):
        self._update_insterval = None
        self.set()
        self._update_thread()

    def _update_thread(self):
        if self._update_insterval:
            pass
        return

    def set(self):
        state = ModelDatabaseRouter().check_mssql_connection()
        cache.set(self.MSSQL_AVAILABLE, state, None)
        return state

    def set_false(self):
        state = False
        cache.set(self.MSSQL_AVAILABLE, state, None)
        return state

    def get(self):
        state = cache.get(self.MSSQL_AVAILABLE, None)
        if state is None:
            return self.set()
        return state


global_state = GlobalState()
