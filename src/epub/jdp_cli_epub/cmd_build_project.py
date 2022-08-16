from pathlib import Path, PurePath
from ebooklib import epub

from .lib_epub_project import get_epub_project
from .lib_epub_style import get_epub_style
from .lib_epub_font import get_epub_font
from .lib_epub_image import get_epub_image

import pprint

def cmd_build_project(config='jdp-book.toml', filename=None):
    cfg = get_epub_project(config=config)
    p = cfg.project.parent

    if filename:
        cfg.filename = Path(filename).absolute()

    # pprint.pprint(cfg)

    book = epub.EpubBook()

    book.set_identifier(cfg.identifier)
    book.set_title(cfg.title)
    book.set_language(cfg.language)

    for author in cfg.author:
        book.add_author(author)

    for stylesheet in cfg.stylesheet:
        book.add_item(get_epub_style(p/stylesheet))

    for font in cfg.font:
        book.add_item(get_epub_font(p/font))

    for image in cfg.image:
        book.add_item(get_epub_image(p/image))

    book.spine = ['nav']

    book.toc = []

    book.add_item(epub.EpubNcx())
    
    nav = epub.EpubNav()

    book.add_item(nav)

    cfg.filename.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(cfg.filename, book, {})
