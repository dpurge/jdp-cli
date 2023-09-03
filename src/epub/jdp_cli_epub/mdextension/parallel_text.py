import re

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
import xml.etree.ElementTree as etree

class ParallelTextProcessor(BlockProcessor):

    RE_FENCE_START = re.compile(r'^:{3,}\s*Start-ParallelText\s*(\n|$)', re.MULTILINE | re.DOTALL)
    RE_FENCE_END = re.compile(r'^\s*:{3,}\s*End-ParallelText\s*(\n|$)', re.MULTILINE | re.DOTALL)

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):

        for block_num, block in enumerate(blocks):

            if re.search(self.RE_FENCE_END, block):

                blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)

                text_element = etree.SubElement(parent, 'div')
                text_element.set('class', 'parallel-text')

                next_block = True
                for _ in range(0, block_num + 1):
                    block = blocks.pop(0)
                    block = block.strip()

                    if block:
                        
                        if next_block:
                            row_element = etree.SubElement(text_element, 'div')
                            row_element.set('class', 'parallel-block')

                        block_element = etree.SubElement(row_element, 'div')
                        block_element.set('class', 'parallel-cell text' if next_block else 'parallel-cell translation')
                        self.parser.parseBlocks(block_element, [block])
                        next_block = not next_block

                return True
            
        # Closing fence not found!  Do nothing...
        return False


class ParallelTextExtension(Extension):

    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(ParallelTextProcessor(md.parser), 'paralleltext', 28)


def makeExtension(**kwargs):
    return ParallelTextExtension(**kwargs)