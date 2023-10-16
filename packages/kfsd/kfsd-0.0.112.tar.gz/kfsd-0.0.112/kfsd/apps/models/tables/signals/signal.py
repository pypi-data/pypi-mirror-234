from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel


class Signal(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    delivery = models.CharField(max_length=MAX_LENGTH)
    is_retain = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.identifier = "SIGNAL={}".format(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Signal"
        verbose_name_plural = "Signals"
