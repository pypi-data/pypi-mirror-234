from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.models.tables.requests.template import (
    RequestTemplate,
    get_request_template_id,
)


def get_endpoint_id(template_name, endpoint_name, method):
    id = ""
    if template_name:
        id += get_request_template_id(template_name) + ","
    id += ",".join(
        [
            "{}={}".format("ENDPOINT", endpoint_name),
            "{}={}".format("METHOD", method),
        ]
    )
    return id


class Endpoint(BaseModel):
    METHOD_CHOICES = (
        ("POST", "POST"),
        ("GET", "GET"),
        ("DELETE", "DELETE"),
    )
    name = models.CharField(max_length=MAX_LENGTH)
    request_template = models.ForeignKey(
        RequestTemplate, on_delete=models.CASCADE, blank=True, null=True
    )
    url = models.TextField()
    method = models.CharField(
        choices=METHOD_CHOICES, default="GET", max_length=MAX_LENGTH
    )
    body = models.ForeignKey(
        Data,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="data",
    )
    success_code = models.IntegerField()

    def save(self, *args, **kwargs):
        template_name = ""
        if self.request_template:
            template_name = self.request_template.name
        self.identifier = get_endpoint_id(template_name, self.name, self.method)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"
