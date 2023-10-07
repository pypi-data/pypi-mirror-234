from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel


def get_header_id(name, key):
    return ",".join(
        [
            "{}={}".format("NAME", name),
            "{}={}".format("HEADER", key),
        ]
    )


class Header(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    key = models.CharField(max_length=MAX_LENGTH)
    value = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.identifier = get_header_id(self.name, self.key)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Header"
        verbose_name_plural = "Headers"
