from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.settings.config import Config
from kfsd.apps.models.tables.requests.endpoint import Endpoint


class Remote(BaseModel):
    config = models.OneToOneField(
        Config, on_delete=models.CASCADE, related_name="remote"
    )
    endpoint = models.ForeignKey(
        Endpoint, on_delete=models.PROTECT, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.identifier = self.config.identifier
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Remote"
        verbose_name_plural = "Remote"
