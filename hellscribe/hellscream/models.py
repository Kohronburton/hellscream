from django.db import models


class WorkPacket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(blank=False, null=False)
