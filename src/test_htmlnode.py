import unittest
from src.htmlnode import *

class TestHTMLNode(unittest.TestCase):

    # Test props_to_html method: ensure output matches expected HTML attribute string format.
    def test_props_to_html_basic_io(self):
        node = HTMLnode(
            tag='a',
            value='Link',
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    # Test __repr__ method: ensure output matches the expected string representation of the node.
    def test_HTMLnode_repr(self):
        node2 = HTMLnode(
            tag="a",
            value="Link",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = "HTML-node(a, Link, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node2.__repr__(), expected)

    # Test to_html method: should raise NotImplementedError since it's not yet implemented.
    def test_HTMLnode_tohtml(self):
        node3 = HTMLnode()
        with self.assertRaises(NotImplementedError):
            node3.to_html()
    
    # Test to_html in LeafNode - No value: Should raise a ValueError as there's no value.
    def test_leaf_node_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    # Test to_html in LeafNode - No tag: Should return the value as a plaintext string. 
    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode(None, "This is a test!")
        expected = "This is a test!"
        self.assertEqual(node.to_html(), expected)
    
    # Test to_html in LeadMode - all present: Should return html formatted string.
    #  string should match: <a "href="www.google.com">This is a test!</a>
    def test_leaf_node_to_html_with_all(self):
        node = LeafNode("a", "This is a test!", {"href":"www.google.com"})
        expected = "<a href=\"www.google.com\">This is a test!</a>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_node_to_html_with_all(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

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
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_deep_nested_structure(self):
        deep_tree = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("section", [
                    LeafNode("p", "Paragraph 1"),
                    ParentNode("div", [
                        LeafNode("p", "Paragraph 2"),
                        LeafNode("p", "Paragraph 3"),
                    ])
                ])
            ]
        )
        expected = (
            "<div><h1>Title</h1><section><p>Paragraph 1</p>"
            "<div><p>Paragraph 2</p><p>Paragraph 3</p></div></section></div>"
        )
        self.assertEqual(deep_tree.to_html(), expected)
    
    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Content")],
            props={"class": "main", "id": "header"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="main" id="header">Content</div>'
        )
        
    def test_to_html_with_invalid_child_type(self):
        class Dummy:
            pass
        dummy = Dummy()
        node = ParentNode("div", [dummy])
        with self.assertRaises(AttributeError):  # Or a custom error
            node.to_html()
            print(node.to_html)

    def test_mixed_valid_and_invalid_children(self):
        valid = LeafNode("p", "text")
        class Dummy: pass
        dummy = Dummy()
        node = ParentNode("div", [None, valid, dummy])
        with self.assertRaises(AttributeError):  # Adjust if custom error added
            node.to_html()
    

# Run the unit tests when this file is executed
if __name__ == "__main__":
    unittest.main()