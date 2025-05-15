import unittest
from src.htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic_io(self):
        node = HTMLnode(
            tag='a',
            value='Link',
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node2 = HTMLnode(
            tag="a",
            value="Link",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = "HTML-node(a, Link, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node2.__repr__(), expected)

    def test_tohtml(self):
        node3 = HTMLnode()
        with self.assertRaises(NotImplementedError):
            node3.to_html()
