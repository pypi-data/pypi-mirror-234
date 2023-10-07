from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.rabbitmq.exchange import Exchange


class Route(BaseModel):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    routing_key = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.identifier = "{}={}".format("ROUTE", self.routing_key)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Route"
        verbose_name_plural = "Routes"
