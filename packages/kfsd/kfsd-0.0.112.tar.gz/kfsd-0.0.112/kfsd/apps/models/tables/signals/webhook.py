from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.core.utils.system import System
from kfsd.apps.models.tables.requests.endpoint import Endpoint


class Webhook(BaseModel):
    signal = models.ForeignKey(
        Signal, on_delete=models.CASCADE, related_name="webhooks"
    )
    endpoint = models.ForeignKey(Endpoint, on_delete=models.PROTECT)
    uniq_id = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.uniq_id = System.api_key(10)
            self.identifier = "{}={}".format("ID", self.uniq_id)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Webhook"
        verbose_name_plural = "Webhooks"
