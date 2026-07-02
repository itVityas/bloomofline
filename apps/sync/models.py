from django.db import models


class SyncDate(models.Model):
    last_sync = models.DateTimeField()

    def __str__(self):
        return str(self.last_sync)

    class Meta:
        ordering = ["-id"]
        app_label = "sync"
