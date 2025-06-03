import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
#these test the HTMLNode class.
    def test_eq_props(self):
        node = HTMLNode(props={"href": "https://this_is_a_test.com"})
        node2 = ' href="https://this_is_a_test.com"'
        self.assertEqual(node.props_to_html(), node2)

    def test_eq_multi_props(self):
        node = HTMLNode(props={"href": "https://this_is_a_test.com",
                               "target": "_blank"})
        node2 = ' href="https://this_is_a_test.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node2)

    def test_props_None(self):
        node = HTMLNode(props=None)
        node2 = ""
        self.assertEqual(node.props_to_html(), node2)

#these test the LeafNode child class.
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a test.")
        self.assertEqual(node.to_html(), "<p>This is a test.</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a test.")
        self.assertEqual(node.to_html(), "<a>This is a test.</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is a test.")
        self.assertEqual(node.to_html(), "This is a test.")

if __name__ == "__main__":
    unittest.main()