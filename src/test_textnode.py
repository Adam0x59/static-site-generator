import unittest
from src.textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a test node - not equal", TextType.LINK, "www.great-times.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    
    def test_no_url(self):
        node_url_fail = TextNode("This is a text node", TextType.LINK)
        node_url_fail2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertIsNone(node_url_fail.url)
        self.assertIsNone(node_url_fail2.url)

    def test_repr(self):
        node_repr = TextNode("This is a test node", TextType.LINK, "www.great-times.com")
        expected = "TextNode(This is a test node, [anchor text](URL), www.great-times.com)"
        self.assertEqual(node_repr.__repr__(), expected)

if __name__ == "__main__":
    unittest.main()
