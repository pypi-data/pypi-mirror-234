from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.rabbitmq.route import Route


class Queue(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    is_declare = models.BooleanField(default=False)
    is_consume = models.BooleanField(default=True)
    declare_attrs = models.JSONField(default=dict)
    consume_attrs = models.JSONField(default=dict)
    routes = models.ManyToManyField(Route)

    def save(self, *args, **kwargs):
        self.identifier = "{}={}".format("QUEUE", self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Queue"
        verbose_name_plural = "Queue"
