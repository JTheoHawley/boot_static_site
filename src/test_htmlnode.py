import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()