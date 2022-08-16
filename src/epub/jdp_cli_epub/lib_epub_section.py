import jinja2
import markdown

from pathlib import Path
from ebooklib import epub
from ebooklib.epub import EpubHtml
from lxml.html import fromstring

from .lib_epub_tools import uid_for_path #, media_type_for_filename
# from knack.util import CLIError

def get_epub_section(text: Path, template: Path, sequence):

    templateLoader = jinja2.FileSystemLoader(searchpath=template)
    templateEnv = jinja2.Environment(loader=templateLoader)

    md = markdown.Markdown(extensions=[
        'tables',
        'full_yaml_metadata',
        'attr_list'])

    sec = None
    txt = None

    if text.exists():
        with open(text, encoding='utf-8') as f:
            txt = f.read()
            html = md.convert(txt)
            meta = getattr(md, "Meta")
            md.reset()

        if meta.get('ready', False):
            tpl = templateEnv.get_template(
                '{template}.html'.format(template = meta.get('template', 'section')))
            lang = meta.get('lang', 'en')
            html = tpl.render(contents = html, meta = meta)

            doc = fromstring(html)

            fn = 'section-{:0>4}.xhtml'.format(next(sequence))
            uid = uid_for_path(fn)
            title = doc.find(".//h1").text
            txt = EpubHtml(
                uid = uid,
                file_name = fn,
                title = title,
                lang = lang)
            txt.content = html
            style = meta.get('style')
            if style:
                txt.add_link(href='style/{style}.css'.format(style=style), rel='stylesheet', type='text/css')
            sec = epub.Section(title, fn)

    return sec, txt
