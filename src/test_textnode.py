import unittest

from textnode import TextNode, TextType
from node_delimiter import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
#these test textnode.py
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.test.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.test.com")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not not a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.test.com")
        self.assertNotEqual(node, node2)

    def test_noteq_url2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.badtest.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.test.com")
        self.assertNotEqual(node, node2)

#these test node_delimiter.py
    def test_delim_bold(self):
        node = TextNode("this is a **BOLD** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("this is a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" word.", TextType.TEXT)],
            new_nodes
        )

    def test_delim_double_bold(self):
        node = TextNode("this **is** a **BOLD** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("this ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" word.", TextType.TEXT)],
            new_nodes
        )

    def test_delim_italic_and_bold(self):
        node = TextNode("this is a **BOLD** and a _ITALIC_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("this is a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("ITALIC", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_delim_uneven_delimiter(self):
        node = TextNode("this **is** a **BOLD* word.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
            
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()