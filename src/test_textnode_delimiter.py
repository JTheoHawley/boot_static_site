import unittest

from textnode import TextNode, TextType
from node_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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

#these test split_nodes_image
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )


#these test split_nodes_link

    def test_split_links(self):
        node = TextNode(
            "This is text with an [test link](https://www.test.com) and another [test link2](https://www.test2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("test link", TextType.LINK, "https://www.test.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "test link2", TextType.LINK, "https://www.test2.com"
                ),
            ],
            new_nodes,
        )

#these test text_to_textnodes
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertListEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()