from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel


class Exchange(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    attrs = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.identifier = "{}={}".format("EXCHANGE", self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Exchange"
        verbose_name_plural = "Exchanges"
