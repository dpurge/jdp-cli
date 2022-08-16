import jinja2
import markdown

from pathlib import Path
from ebooklib.epub import EpubHtml
from lxml.html import fromstring

from .mdextension import VocabularyListExtension, DialogListExtension
from .lib_epub_tools import uid_for_path

def get_epub_text(text, template, sequence):
    txt = None

    templateLoader = jinja2.FileSystemLoader(searchpath=template)
    templateEnv = jinja2.Environment(loader=templateLoader)

    md = markdown.Markdown(extensions=[
        'footnotes',
        'tables',
        'full_yaml_metadata',
        'attr_list',
        VocabularyListExtension(),
        DialogListExtension()])

    with open(text, encoding='utf-8') as f:
        txt = f.read()
        html = md.convert(txt)
        meta = getattr(md, "Meta")
        md.reset()

    if meta.get('ready', False):
        tpl = templateEnv.get_template(
            '{template}.html'.format(template = meta.get('template', 'default')))
        lang = meta.get('lang', 'en')
        html = tpl.render(contents = html, meta = meta)

        doc = fromstring(html)

        fn = 'text-{:0>4}.xhtml'.format(next(sequence))
        uid = uid_for_path(fn)
        txt = EpubHtml(
            uid = uid,
            file_name = fn,
            title = doc.find(".//h1").text,
            lang = lang)
        txt.content = html

        style = meta.get('style')
        if style:
            txt.add_link(href='style/{style}.css'.format(style=style), rel='stylesheet', type='text/css')

    return txt
