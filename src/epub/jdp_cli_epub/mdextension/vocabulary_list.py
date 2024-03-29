"""
Modified from: https://raw.githubusercontent.com/Python-Markdown/markdown/master/markdown/extensions/def_list.py

Original code Copyright 2008 [Waylan Limberg](http://achinghead.com)

Additional changes Copyright 2008-2014 The Python Markdown Project

All changes Copyright 2019 LangProject

License: [BSD](https://opensource.org/licenses/bsd-license.php)
"""

import re

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
import xml.etree.ElementTree as etree

class VocabularyListProcessor(BlockProcessor):

    RE = re.compile(r'(^|\n)[ ]{0,3}:[ ]{1,3}(.*?)(\n|$)')
    NO_INDENT_RE = re.compile(r'^[ ]{0,3}[^ :]')
    DESCRIPTION_RE = re.compile(r'^(\s*{(?P<grammar>[^}]+)})?(\s*\[(?P<transcription>[^\]]+)\])?\s*(?P<translation>[^\(\)]*)?\s*(?P<notes>\([^\(\)]*\))?$')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):

        raw_block = blocks.pop(0)
        m = self.RE.search(raw_block)
        terms = [l.strip() for l in
                 raw_block[:m.start()].split('\n') if l.strip()]
        block = raw_block[m.end():]

        no_indent = self.NO_INDENT_RE.match(block)
        if no_indent:
            d, theRest = (block, None)
        else:
            d, theRest = self.detab(block)

        if d:
            d = '{}\n{}'.format(m.group(2), d)
        else:
            d = m.group(2)
        sibling = self.lastChild(parent)
        if not terms and sibling is None:
            # This is not a definition item. Most likely a paragraph that
            # starts with a colon at the beginning of a document or list.
            blocks.insert(0, raw_block)
            return False
        if not terms and sibling.tag == 'p':
            # The previous paragraph contains the terms
            state = 'looselist'
            terms = sibling.text.split('\n')
            parent.remove(sibling)
            # Acquire new sibling
            sibling = self.lastChild(parent)
        else:
            state = 'list'

        if sibling is not None and sibling.tag == 'dl':
            # This is another item on an existing list
            dl = sibling
            if not terms and len(dl) and dl[-1].tag == 'dd' and len(dl[-1]):
                state = 'looselist'
        else:
            # This is a new list
            dl = etree.SubElement(parent, 'dl')
            dl.set('class', 'vocabulary-list')

        # Add terms
        for term in terms:
            dt = etree.SubElement(dl, 'dt')
            dt.set('class', 'vocabulary-phrase')
            dt.text = term

        # Add definition
        self.parser.state.set(state)

        dd = etree.SubElement(dl, 'dd')
        dd.set('class', 'vocabulary-definition')
        description = self.DESCRIPTION_RE.match(d)
        if description:
            grammar_text = description.group('grammar')
            if grammar_text:
                grammar = etree.SubElement(dd, 'span')
                grammar.set('class', 'vocabulary-grammar')
                grammar.text = grammar_text.strip()
                grammar.tail = ' '

            transcription_text = description.group('transcription')
            if transcription_text:
                transcription = etree.SubElement(dd, 'span')
                transcription.set('class', 'vocabulary-transcription')
                transcription.text = transcription_text.strip()
                transcription.tail = ' '

            translation_text = description.group('translation')
            if translation_text:
                translation = etree.SubElement(dd, 'span')
                translation.set('class', 'vocabulary-translation')
                self.parser.parseBlocks(translation, [translation_text.strip()])

            notes_text = description.group('notes')
            if notes_text:
                notes = etree.SubElement(dd, 'span')
                notes.set('class', 'vocabulary-notes')
                notes_text = notes_text.lstrip('( ')
                notes_text = notes_text.rstrip(' )')
                self.parser.parseBlocks(notes, [notes_text])
        else:
            # this should never happen, but keep it just in case of an error in regexp
            self.parser.parseBlocks(dd, [d])

        self.parser.state.reset()

        if theRest:
            blocks.insert(0, theRest)

class VocabularyListIndentProcessor(ListIndentProcessor):

    ITEM_TYPES = ['dd']
    LIST_TYPES = ['dl']

    def create_item(self, parent, block):
        dd = etree.SubElement(parent, 'dd')
        self.parser.parseBlocks(dd, [block])
    
class VocabularyListExtension(Extension):

    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(VocabularyListIndentProcessor(md.parser), 'vocabularyindent', 86)
        md.parser.blockprocessors.register(VocabularyListProcessor(md.parser), 'vocabularylist', 26)

def makeExtension(**kwargs):
    return VocabularyListExtension(**kwargs)