from django.db.backends.sqlite3 import base


class DatabaseWrapper(base.DatabaseWrapper):
    def _start_transaction_under_autocommit(self):
        """
        Starts a transaction with BEGIN IMMEDIATE to grab the write lock
        upfront, preventing 'database is locked' errors under concurrency.
        """
        self.cursor().execute("BEGIN IMMEDIATE")
