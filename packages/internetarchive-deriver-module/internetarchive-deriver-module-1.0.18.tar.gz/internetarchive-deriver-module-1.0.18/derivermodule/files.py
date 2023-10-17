import pathlib

from .const import PB_ITEM

def canonical_item_filename(filepath):
    """
    Normalises an absolute path to a file in the container to a canonical path.
    For example '/item/test_item/test_directory/test_file_hocr.html.gz' would be
    turned into 'test_item/test_directory/test_file_hocr.html.gz'.

    Args:

    * filepath (``str``): Absolute path to the file within the container

    Returns:

    * canonical path (``str``)
    """
    root = pathlib.Path(PB_ITEM)
    item_path = pathlib.Path(filepath)
    rel = item_path.relative_to(root)

    return str(rel)
