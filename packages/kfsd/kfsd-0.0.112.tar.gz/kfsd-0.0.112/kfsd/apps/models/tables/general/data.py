from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.general.file import File


class Data(BaseModel):
    SOURCE_TYPE_CHOICES = (
        ("RAW", "RAW"),
        ("FILE", "FILE"),
    )
    name = models.CharField(max_length=MAX_LENGTH)
    is_template = models.BooleanField(default=False)
    default_template_values = models.JSONField(default=dict)
    content_type = models.CharField(max_length=MAX_LENGTH)
    source_type = models.CharField(
        max_length=MAX_LENGTH, choices=SOURCE_TYPE_CHOICES, default="RAW"
    )
    raw_body = models.TextField(blank=True, null=True)
    raw_json_body = models.JSONField(default=dict)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.identifier = ",".join(
            [
                "{}={}".format("DATA", self.name),
            ]
        )
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Data"
        verbose_name_plural = "Data"
