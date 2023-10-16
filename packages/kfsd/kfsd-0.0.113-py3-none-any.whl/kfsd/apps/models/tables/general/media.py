from django.db import models

from kfsd.apps.core.utils.system import System
from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.general.source import Source


# Github, Twitter, Linkedin, Youtube, Website
class Media(BaseModel):
    link = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    media_id = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.media_id = System.api_key(6)
        if self.source:
            self.identifier = "{},MEDIA_ID={}".format(
                self.source.identifier, self.media_id
            )
        else:
            self.identifier = "MEDIA_ID={}".format(self.media_id)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Media"
        verbose_name_plural = "Media"
