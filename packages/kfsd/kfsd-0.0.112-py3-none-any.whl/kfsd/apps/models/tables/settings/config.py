from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH


class Config(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    version = models.CharField(max_length=MAX_LENGTH)
    is_local_config = models.BooleanField(default=True)
    lookup_dimension_keys = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.identifier = ",".join(
            [
                "{}={}".format("CONFIG", self.name),
                "{}={}".format("VERSION", self.version),
            ]
        )
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Config"
        verbose_name_plural = "Configs"
