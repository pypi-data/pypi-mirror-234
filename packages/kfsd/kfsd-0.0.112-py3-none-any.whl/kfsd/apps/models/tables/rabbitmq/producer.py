from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.core.utils.system import System


class Producer(BaseModel):
    signal = models.ForeignKey(
        Signal, on_delete=models.CASCADE, related_name="producers"
    )
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    properties = models.JSONField(default=dict)
    uniq_id = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.uniq_id = System.api_key(10)
            self.identifier = "{}={}".format("ID", self.uniq_id)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Route"
        verbose_name_plural = "Routes"


def construct_producer_attrs(id):
    producer = Producer.objects.get(identifier=id)
    publishAttrs = {
        "exchange": producer.route.exchange.name,
        "routing_key": producer.route.routing_key,
        "properties": producer.properties,
    }
    return publishAttrs
