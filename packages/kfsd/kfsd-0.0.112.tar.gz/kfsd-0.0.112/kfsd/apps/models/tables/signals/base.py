from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.core.utils.system import System
from kfsd.apps.core.utils.time import Time
from kfsd.apps.models.constants import MAX_LENGTH


class BaseSignal(BaseModel):
    class Meta:
        abstract = True

    STATUS_CHOICES = (
        ("P", "PENDING"),
        ("I", "IN-PROGRESS"),
        ("E", "ERROR"),
        ("C", "COMPLETED"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    attempts = models.IntegerField(default=0)
    debug_info = models.JSONField(default=dict)
    name = models.CharField(max_length=MAX_LENGTH)
    data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = System.uuid(32)
        return super().save(*args, **kwargs)


def log_error(instance, error):
    oldDebugInfo = instance.debug_info
    currentTimeStr = Time.calculate_time(Time.current_time(), {"minutes": 0}, True)
    oldDebugInfo[currentTimeStr] = error
    instance.debug_info = oldDebugInfo
    instance.attempts += 1
    instance.status = "E"
    instance.save()
