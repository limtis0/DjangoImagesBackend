from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from hexOceanBackend.settings import STATIC_URL
from pathlib import Path


def save_image_locally(self, filename):
    extension = filename.split('.')[-1]
    return Path(f'{STATIC_URL}{self.user.username}/{self.uuid}/original.{extension}')


class Image(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=22)
    image = models.ImageField(upload_to=save_image_locally,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
