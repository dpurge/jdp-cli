from ebooklib.epub import EpubItem

from .lib_epub_tools import uid_for_path, media_type_for_filename
from knack.util import CLIError

def get_epub_image(filename):

    if not filename.is_file():
        raise CLIError(f'Image file does not exist: {filename.absolute()}')

    fn = f'image/{filename.name}'
    uid = uid_for_path(fn)

    with open(filename, mode='rb') as f:
        image = EpubItem(
            uid = uid,
            file_name = fn,
            media_type = media_type_for_filename(filename),
            content = f.read())

    return image
    