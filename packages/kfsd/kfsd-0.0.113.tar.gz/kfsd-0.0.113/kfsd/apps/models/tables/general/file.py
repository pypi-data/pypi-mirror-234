from django.db import models
from django.utils.text import slugify

from kfsd.apps.models.constants import (
    MAX_LENGTH,
    MIN_LENGTH,
    FILE,
    FILE_NAME_REGEX_CONDITION,
)
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.core.utils.system import System


class File(BaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=FILE_NAME_REGEX_CONDITION,
                message="file name doesnt match condition {}".format(
                    FILE_NAME_REGEX_CONDITION
                ),
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    slug = models.SlugField()
    # uniq id to solve same file names
    uniq_id = models.CharField(max_length=MAX_LENGTH)
    file = models.FileField(upload_to="uploads/")
    is_public = models.BooleanField(default=False)
    version = models.CharField(max_length=MAX_LENGTH)
    expiry_in_mins = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.name = self.file.name
            self.slug = slugify(self.name)
            self.uniq_id = System.api_key(6)
            self.identifier = "{}={},VER={},UNIQ_ID={}".format(
                FILE, self.name, self.version, self.uniq_id
            )

        return super().save(*args, **kwargs)
