from tempfile import NamedTemporaryFile
from typing import Tuple
from PIL import Image


def generate_image(suffix: str, size: Tuple[int, int]):
    image = Image.new('RGB', size)
    tmp_file = NamedTemporaryFile(suffix=suffix)
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file
