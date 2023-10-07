import os
from typing import Union


class FathomException(Exception):
    """A client exception"""


class TaskNotCompleteException(FathomException):
    """Tried to download the result from a task that was not complete"""


def write_tiff_data_to_file(geotiff_bytes, layer_id, output_dir, pattern, tiff_num):
    format_vars = {
        "sep": os.sep,
        "layer_id": layer_id,
        "tiff_num": tiff_num,
    }
    base = pattern.format(**format_vars)
    filename = os.path.join(output_dir, base)
    tiff_dir = os.path.dirname(filename)
    os.makedirs(tiff_dir, exist_ok=True)
    with open(filename, "wb") as shapefile:
        shapefile.write(geotiff_bytes)


PathOrString = Union[os.PathLike, str]
