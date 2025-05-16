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

# Run the unit tests when this file is executed
if __name__ == "__main__":
    unittest.main()