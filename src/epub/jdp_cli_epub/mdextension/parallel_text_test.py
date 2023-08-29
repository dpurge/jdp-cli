import unittest
from markdown import test_tools
from xml.etree import ElementTree as etree

class ParallelTextExtension_Test(test_tools.TestCase):
    def setUp(self):
        self.default_kwargs = dict(
            extensions = [
                'parallel_text',
            ],
        )

    def assertMarkdown(self, markdown, html, **kwds):
        self.assertMarkdownRenders(
            self.dedent(markdown),
            self.dedent(html),
            **kwds)

    def test_header_with_space(self):
        self.assertMarkdown("""\
            ::: Start-ParallelText
                            
            ::: End-ParallelText
            """, """\
            <div class="parallel-text"></div>
            """)

    def test_header_without_space(self):
        self.assertMarkdown("""\
            :::Start-ParallelText
                            
            :::End-ParallelText
            """, """\
            <div class="parallel-text"></div>
            """)

    def test_one_pair_of_paragraphs_with_breaks(self):
        self.assertMarkdown(
            """\
            ::: Start-ParallelText

            This is line A1.
            This is line A2.
                
            This is line B1.
            This is line B2.

            ::: End-ParallelText
            """,
            """\
            <div class="parallel-text">
            <div class="parallel-row">
            <div class="parallel-block-left">
            <p>This is line A1.
            This is line A2.</p>
            </div>
            <div class="parallel-block-right">
            <p>This is line B1.
            This is line B2.</p>
            </div>
            </div>
            </div>
            """)

    def test_one_pair_of_paragraphs_without_breaks(self):
        self.assertMarkdown(
            """\
            ::: Start-ParallelText
            This is line A1.
            This is line A2.
                
            This is line B1.
            This is line B2.
            ::: End-ParallelText
            """,
            """\
            <div class="parallel-text">
            <div class="parallel-row">
            <div class="parallel-block-left">
            <p>This is line A1.
            This is line A2.</p>
            </div>
            <div class="parallel-block-right">
            <p>This is line B1.
            This is line B2.</p>
            </div>
            </div>
            </div>
            """)
        
if __name__ == '__main__':
    unittest.main()