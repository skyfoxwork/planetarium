import pathlib
import uuid

from django.utils.text import slugify


def astronomy_show_image_path(astronomy_show, filename: str) -> pathlib.Path:
    file_name = (f"{slugify(astronomy_show.title)}-{uuid.uuid4()}"
                 f"{pathlib.Path(filename).suffix}")
    return pathlib.Path("uploads/images/") / pathlib.Path(file_name)
