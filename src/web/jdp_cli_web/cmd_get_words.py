from collections import Counter
from .lib_get_text_from_html import lib_get_text_from_html
from .lib_get_words_from_chunks import lib_get_words_from_chunks

def cmd_get_words(uri):
    chunks = lib_get_text_from_html(uri)
    words = lib_get_words_from_chunks(chunks)
    counter = Counter(words)
    return counter
