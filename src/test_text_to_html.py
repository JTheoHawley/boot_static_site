import unittest

from textnode import TextNode, TextType
from text_to_html import (text_node_to_html_node, extract_markdown_images, extract_markdown_links)

#these test text_node_to_html_node
class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "This is a image node"})

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://link.com"})

    #these test extract_markdown_images
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_multi(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image](https://i.imgur.com/zjjcJKZ2.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ2.png")], matches)


    #these test extract_markdown_links
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_link_multi(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to something](https://www.something.com)"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to something", "https://www.something.com")], matches)

    #these test both the above extracts
    def test_extract_markdown_image_and_link(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to something](https://www.something.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        self.assertListEqual([("to something", "https://www.something.com")], link_matches)

    def test_images_not_captured_as_links(self):
        text = "![image](https://example.com/pic.jpg)"
        # Should find no links since this is an image
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_no_matches(self):
        text = "This is just plain text with no markdown"
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_incomplete_syntax(self):
    # Missing closing bracket or parenthesis
        text = "![incomplete image and [incomplete link"
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))



if __name__ == "__main__":
    unittest.main()