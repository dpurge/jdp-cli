from .lib_get_text_from_html import lib_get_text_from_html

def cmd_get_text(uri):
    chunks = lib_get_text_from_html(uri)
    text = ' '.join(chunks)
    return text
