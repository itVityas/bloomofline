from django.db import models


class OfflineOneCTTN(models.Model):
    number = models.CharField(max_length=50)
    series = models.CharField(max_length=50, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "aonec"
        ordering = ['-id']

    def __str__(self):
        return self.number


class OfflineOneCTTNItem(models.Model):
    onec_ttn = models.ForeignKey(OfflineOneCTTN, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "aonec"
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} ({self.count})"
