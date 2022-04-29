import requests
from bs4 import BeautifulSoup

def lib_get_text_from_html(uri):
    res = requests.get(uri)
    html_content = res.content
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.find_all(text=True)

    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
        # there may be more elements you don't want, such as "style", etc.
    ]

    chunks = (t for t in text if t.parent.name not in blacklist)
    # for t in text:
    #     if t.parent.name not in blacklist:
    #         output += '{} '.format(t)

    return chunks