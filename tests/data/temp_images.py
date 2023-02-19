from tempfile import NamedTemporaryFile
from typing import Tuple
from PIL import Image as PILImage
from images.models import Image
from shutil import rmtree


def generate_image(suffix: str, size: Tuple[int, int]):
    image = PILImage.new('RGB', size)
    tmp_file = NamedTemporaryFile(suffix=suffix)
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


def cleanup_images():
    for image in Image.objects.all():
        rmtree(image.get_directory_path())
