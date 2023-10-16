from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel


def get_param_id(name, key):
    return ",".join(
        [
            "{}={}".format("NAME", name),
            "{}={}".format("PARAM", key),
        ]
    )


class Param(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    key = models.CharField(max_length=MAX_LENGTH)
    value = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.identifier = get_param_id(self.name, self.key)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Param"
        verbose_name_plural = "Params"
