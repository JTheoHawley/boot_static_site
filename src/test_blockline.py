import unittest
from blockline import (markdown_to_blocks, block_to_block_type, 
                    BlockType, markdown_to_html_node,
                    paragraph_to_html_node, quote_to_html_node,
                    heading_to_html_node,)

class Test_blockline(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
#these test block_to_block_type
    def test_block_to_block_type_ordered_valid(self):
        block = """1. First
2. Second
3. Third"""

        is_ordered = block_to_block_type(block)
        self.assertEqual(is_ordered, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_invalid_iterable(self):
        block = """1. First
two. Second
3. Third"""

        is_not_ordered = block_to_block_type(block)
        self.assertEqual(is_not_ordered, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_invalid_order(self):
        block = """1. First
3. Third"""

        is_not_ordered = block_to_block_type(block)
        self.assertEqual(is_not_ordered, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = """# 1"""

        is_heading = block_to_block_type(block)
        self.assertEqual(is_heading, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = """```"code"```"""

        is_code = block_to_block_type(block)
        self.assertEqual(is_code, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = """> This is a quote
> This is also a quote"""

        is_quote = block_to_block_type(block)
        self.assertEqual(is_quote, BlockType.QUOTE)

    def test_block_to_block_type_unordered(self):
        block = """- First item
- Second item"""

        is_unordered = block_to_block_type(block)
        self.assertEqual(is_unordered, BlockType.UNORDERED_LIST)

#these test markdown_to_html_node and helper functions
    def test_markdown_to_html_paragraph(self):
        md_p = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        expected = (
    "<div><p>This is <b>bolded</b> paragraph</p>"
    "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here\n"
    "This is the same paragraph on a new line</p></div>"
)
        converted = markdown_to_html_node(md_p).to_html()
        self.assertEqual(expected, converted)

    def test_markdown_to_html_heading(self):#this test showed a issue when headings were not seperated by "\n\n", be aware.
        md_h = """# Heading One

## Heading Two with _italic_

### **BOLD** Heading Three"""
        expected = (
    "<div>"
    "<h1>Heading One</h1>"
    "<h2>Heading Two with <i>italic</i></h2>"
    "<h3><b>BOLD</b> Heading Three</h3>"
    "</div>"
)
        converted = markdown_to_html_node(md_h).to_html()
        self.assertEqual(expected, converted)

    def test_markdown_to_html_quote(self):
        md_q = """> This is a quote with _italics_ and **bold** text
> And a second quoted line

A normal paragraph after."""
        expected = (
    "<div>"
    "<blockquote>This is a quote with <i>italics</i> and <b>bold</b> text\nAnd a second quoted line</blockquote>"
    "<p>A normal paragraph after.</p>"
    "</div>"
)
        converted = markdown_to_html_node(md_q).to_html()
        self.assertEqual(expected, converted)

    def test_markdown_to_html_code(self):
        md_c = """```
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)
```"""
        expected = (
    "<div><pre><code>def fib(n):\n"
    "    return n if n <= 1 else fib(n-1) + fib(n-2)\n"
    "</code></pre></div>"
)
        converted = markdown_to_html_node(md_c).to_html()
        self.assertEqual(expected, converted)

if __name__ == "__main__":
    unittest.main()