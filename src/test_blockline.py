import unittest
from blockline import markdown_to_blocks, block_to_block_type, BlockType

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




if __name__ == "__main__":
    unittest.main()