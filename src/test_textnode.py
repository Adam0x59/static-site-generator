import unittest
from src.textnode import *


class TestTextNode(unittest.TestCase):
    
    # Test the __eq__ method of the TextNode class.
    # It should return True if two TextNode instances have the same values,
    # and False if they differ.
    def test_TextNode_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a test node - not equal", TextType.LINK, "www.great-times.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    
    # Test that the url attribute is None when not provided.
    def test_TextNode_no_url(self):
        node_url_fail = TextNode("This is a text node", TextType.LINK)
        node_url_fail2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertIsNone(node_url_fail.url)
        self.assertIsNone(node_url_fail2.url)

    # Test the __repr__ method of the TextNode class.
    # It should return a string representation in the expected format.
    def test_TextNode_repr(self):
        node_repr = TextNode("This is a test node", TextType.LINK, "www.great-times.com")
        expected = "TextNode(This is a test node, [anchor text](URL), www.great-times.com)"
        self.assertEqual(node_repr.__repr__(), expected)

# Run the unit tests when this file is executed
if __name__ == "__main__":
    unittest.main()
