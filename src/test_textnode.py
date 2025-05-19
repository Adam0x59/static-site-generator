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
        expected = "TextNode(This is a test node, link, www.great-times.com)"
        self.assertEqual(node_repr.__repr__(), expected)
        
    # Test text_node_to_html fucntion for TEXT type
    def test_txttohtml_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    # Test text_node_to_html fucntion for BOLD type
    def test_txttohtml_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    # Test text_node_to_html fucntion for ITALIC type
    def test_txttohtml_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    # Test text_node_to_html fucntion for CODE type
    def test_txttohtml_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
 
    # Test text_node_to_html fucntion for LINK type
    def test_txttohtml_link(self):
        node = TextNode("This is a link", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href":"www.google.com"})

    # Test text_node_to_html fucntion for IMAGE type
    def test_txttohtml_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"www.google.com", "alt":"This is an image"})

# Run the unit tests when this file is executed
if __name__ == "__main__":
    unittest.main()
