from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.requests.header import Header
from kfsd.apps.models.tables.requests.param import Param


def get_request_template_id(name):
    return "REQ_TEMPLATE={}".format(name)


class RequestTemplate(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    headers = models.ManyToManyField(Header)
    params = models.ManyToManyField(Param)

    def save(self, *args, **kwargs):
        self.identifier = get_request_template_id(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "RequestTemplate"
        verbose_name_plural = "RequestTemplates"
