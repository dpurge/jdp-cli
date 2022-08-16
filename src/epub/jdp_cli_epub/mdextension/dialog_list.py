
import re

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
from markdown.util import etree

class DialogListProcessor(BlockProcessor):

    RE = re.compile(r'(^|\n)((?P<separator>--|@|＠)(?P<speaker>[^:︰：]*)[:︰：])\s*(\n|$)(?P<utterance>(  .*(\n|$))*)?')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):

        dialog = None
        if parent.tag == 'ul' and parent.get('class') == 'dialog':
            dialog = parent
        else:
            last_child = self.lastChild(parent)
            if last_child.tag == 'ul' and last_child.get('class') == 'dialog':
                dialog = last_child

        block = blocks.pop(0)
        m = self.RE.search(block)
        while m:
            start = m.start()
            end = m.end()
            separator_raw = m.group('separator')
            utterance_raw = m.group('utterance')
            
            if start > 0:
                self.parser.parseBlocks(parent, [block[:start]])

            if not dialog:
                dialog = etree.SubElement(parent, 'ul')
                dialog.set('class', 'dialog')

            item = etree.SubElement(dialog, 'li')
            item.set('class', 'dialog-item')
            if separator_raw == '--':
                separator = etree.SubElement(item, 'div')
                separator.set('class', 'dialog-item-separator')
                separator.text = '&mdash;'
            else:
                speaker = etree.SubElement(item, 'div')
                speaker.set('class', 'dialog-item-speaker')
                speaker.text = m.group('speaker').strip()

            utterance = etree.SubElement(item, 'div')
            utterance.set('class', 'dialog-item-utterance')
            if utterance_raw:
                lines = [line[2:] for line in utterance_raw.split('\n')]
                self.parser.parseBlocks(utterance, ['\n'.join(lines)])

            block = block[end:]
            m = self.RE.search(block)
        
        if block:
            self.parser.parseBlocks(parent, [block])



class DialogListIndentProcessor(ListIndentProcessor):

    def test(self, parent, block):
        if block.startswith('  '):
            last_child = self.lastChild(parent)
            if last_child and last_child.tag == 'ul' and last_child.get('class') == 'dialog':
                return True
        return False

    def create_item(self, parent, block):
        dialog = self.lastChild(parent)
        if not dialog.get('class') == 'dialog': raise "Not in a dialog!"
        item = self.lastChild(dialog)
        if not item.get('class') == 'dialog-item': raise "Not in a dialog-item!"
        utterance = self.lastChild(item)
        if not utterance.get('class') == 'dialog-item-utterance': raise "Not in a dialog-item-utterance!"

        utterance_lines = []
        lines = block.split('\n')
        while lines and lines[0].startswith('  '):
            utterance_lines.append(lines.pop(0)[2:])

        self.parser.parseBlocks(utterance, ['\n'.join(utterance_lines)])
        if lines:
            self.parser.parseBlocks(parent, ['\n'.join(lines)])
    
class DialogListExtension(Extension):

    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(DialogListIndentProcessor(md.parser), 'dialogindent', 87)
        md.parser.blockprocessors.register(DialogListProcessor(md.parser), 'dialoglist', 27)

def makeExtension(**kwargs):
    return DialogListExtension(**kwargs)
