# Typing
import datetime
from typing import Dict

# Models
import shortuuid
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

# Routes & Permissions
from images.routes import ImageRouting
from users.permissions import Permissions

# Files & Directories
from hexOceanBackend.settings import STATIC_URL
from pathlib import Path
from PIL import Image as PILImage

# Deletion
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from shutil import rmtree


def image_upload_to(self, _):
    return self.get_file_path()


class Image(models.Model):
    class Meta:
        ordering = ['-title', '-uuid']

    uuid = models.CharField(max_length=22, default=shortuuid.uuid, primary_key=True)
    private_uuid = models.CharField(max_length=22,  # Used for access to original image
                                    default=shortuuid.uuid,
                                    unique=True,
                                    editable=False)
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])

    def get_file_extension(self) -> str:
        return self.image.name.split('.')[-1]

    def get_directory_path(self) -> Path:
        return Path(STATIC_URL, self.user.username, self.uuid)

    def get_file_path(self, extension=None) -> Path:
        # Performance: str.split() may be called multiple times
        if extension is None:
            extension = self.get_file_extension()
        return self.get_directory_path().joinpath(Path(f'{self.private_uuid}.{extension}'))

    def get_thumbnail_file_path(self, thumbnail_size: int, extension=None) -> Path:
        # Performance: str.split() may be called multiple times
        if extension is None:
            extension = self.get_file_extension()

        thumbnail_path = self.get_directory_path().joinpath(Path(f'thumbnail_{thumbnail_size}.{extension}'))

        if not thumbnail_path.exists():
            original_path = self.get_file_path(extension=extension)
            self.create_thumbnail(original_path, thumbnail_path, thumbnail_size)

        return thumbnail_path

    def get_available_thumbnails(self) -> Dict[str, str]:
        thumbnails = {}

        for thumbnail_size in Permissions.iter_allowed_thumbnail_sizes(self.user):
            thumbnails[f"{thumbnail_size}px"] = ImageRouting.get_thumbnail_url(self.user.username,
                                                                               self.uuid,
                                                                               thumbnail_size)
        return thumbnails

    def get_original_media_url(self) -> str:
        return ImageRouting.get_original_media_url(self.user.username, self.uuid)

    @staticmethod
    def create_thumbnail(original_path: Path, thumbnail_path: Path, size: int) -> None:
        image = PILImage.open(original_path)

        width, height = image.size
        scale = height / size
        new_size = (int(width // scale), size)

        thumbnail = image.resize(new_size)
        thumbnail.save(thumbnail_path)


@receiver(pre_delete, sender=Image)
def delete_images(sender, instance, **kwargs):
    rmtree(instance.get_directory_path())


class ExpiringLink(models.Model):
    MIN_DURATION = 300
    MAX_DURATION = 30_000

    image = models.OneToOneField(Image, on_delete=models.CASCADE, primary_key=True)
    duration = models.IntegerField(validators=[
        MinValueValidator(MIN_DURATION),
        MaxValueValidator(MAX_DURATION)
    ])
    valid_until = models.DateTimeField(blank=True)
    uuid = models.CharField(max_length=22, default=shortuuid.uuid)

    def _valid_until_default_value(self) -> datetime:
        return timezone.now() + timezone.timedelta(seconds=self.duration)

    def save(self, *args, **kwargs):
        self.valid_until = self._valid_until_default_value()
        super().save(*args, **kwargs)

    def is_valid(self) -> bool:
        return timezone.now() <= self.valid_until

    def get_expiring_media_url(self):
        return ImageRouting.get_expiring_media_url(username=self.image.user.username, expiring_uuid=self.uuid)
