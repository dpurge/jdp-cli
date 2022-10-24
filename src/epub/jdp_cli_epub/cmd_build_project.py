from pathlib import Path
from ebooklib import epub

from .lib_epub_project import get_epub_project
from .lib_epub_style import get_epub_style
from .lib_epub_font import get_epub_font
from .lib_epub_image import get_epub_image
from .lib_epub_section import get_epub_section
from .lib_epub_text import get_epub_text
# from .lib_epub_tools import sequence
from jdp_cli.lib_cli_tools import sequence

def cmd_build_project(config='jdp-book.toml', filename=None, directory=None):
    cfg = get_epub_project(config=config)
    p = cfg.project.parent

    if filename:
        cfg.filename = Path(filename).absolute()

    if directory:
        cfg.filename = Path(directory).absolute() / cfg.filename.name

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

    section_sequence = sequence()
    text_sequence = sequence()

    for section in cfg.section:
        sec, txt = get_epub_section(text=section.head, template=cfg.template, sequence = section_sequence)
        if sec and txt:
            book.add_item(txt)
            book.spine.append(txt)

            section_texts = []
            for text in section.text:
                txt = get_epub_text(text=text, template=cfg.template, sequence = text_sequence)
                book.add_item(txt)
                book.spine.append(txt)
                section_texts.append(txt)

            book.toc.append((sec, section_texts))

    book.add_item(epub.EpubNcx())
    
    nav = epub.EpubNav()

    book.add_item(nav)

    cfg.filename.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(cfg.filename, book, {})
