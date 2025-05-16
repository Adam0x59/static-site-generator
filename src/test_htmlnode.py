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
    def test_repr(self):
        node2 = HTMLnode(
            tag="a",
            value="Link",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = "HTML-node(a, Link, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node2.__repr__(), expected)

    # Test to_html method: should raise NotImplementedError since it's not yet implemented.
    def test_tohtml(self):
        node3 = HTMLnode()
        with self.assertRaises(NotImplementedError):
            node3.to_html()
