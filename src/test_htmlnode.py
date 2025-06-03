import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

#these test the ParentNode child class
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)
        
    def test_empty_children_list(self):
        node = ParentNode("div", [])
        result = node.to_html()
        self.assertEqual(result, "<div></div>")

    def test_to_html_with_variable_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node, LeafNode(None, "child 2"), LeafNode("p", "child 3")])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span>child 2<p>child 3</p></div>",)
        
    def test_to_html_no_tag(self):
        child_node = LeafNode("b", "child 1")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_child(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_invalid_child(self):
        child_node = LeafNode(None, None)
        node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            node.to_html()
        
    

if __name__ == "__main__":
    unittest.main()